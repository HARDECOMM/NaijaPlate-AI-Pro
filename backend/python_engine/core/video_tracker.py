import math
from collections import defaultdict


def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interW = max(0, xB - xA)
    interH = max(0, yB - yA)
    interArea = interW * interH

    if interArea == 0:
        return 0.0

    boxAArea = max(0, boxA[2] - boxA[0]) * max(0, boxA[3] - boxA[1])
    boxBArea = max(0, boxB[2] - boxB[0]) * max(0, boxB[3] - boxB[1])

    return interArea / float(boxAArea + boxBArea - interArea)


class Track:
    def __init__(self, track_id, box, plate, result, frame_index, frame_path=None):
        self.track_id = track_id
        self.last_box = box
        self.plate = plate
        self.best_result = result
        self.best_score = self._compute_score(result)
        self.hits = 1
        self.state_counts = defaultdict(int)
        self.state_counts[result.get("state", "UNKNOWN")] += 1
        self.first_frame = frame_index
        self.last_frame = frame_index
        self.missed = 0
        self.active = True
        self.best_frame_path = frame_path

    def _compute_score(self, result):
        score_map = {
            "VERIFIED_STATE_MATCH": 100,
            "HIGH_CONFIDENCE_AI": 90,
            "HIGH_CONFIDENCE_STD": 80,
            "REFINED_GUESS": 50,
            "LOW_CONFIDENCE": 20,
            "NONE": 0,
        }

        score = score_map.get(result.get("confidence", "NONE"), 0)
        score += result.get("video_hits", 0) if isinstance(result.get("video_hits"), int) else 0
        return score

    def update(self, box, result, frame_index, frame_path=None):
        self.last_box = box
        self.last_frame = frame_index
        self.hits += 1
        self.state_counts[result.get("state", "UNKNOWN")] += 1
        current_score = self._compute_score(result)

        if current_score >= self.best_score:
            self.best_score = current_score
            self.best_result = result
            if frame_path:
                self.best_frame_path = frame_path
            return True

        return False

    def as_summary(self):
        summary = self.best_result.copy()
        summary["video_track_id"] = self.track_id
        summary["video_hits"] = self.hits
        summary["video_best_frame"] = self.best_frame_path
        summary["video_frames_seen"] = self.last_frame - self.first_frame + 1
        summary["video_state_votes"] = dict(self.state_counts)
        return summary


class VehicleTracker:
    def __init__(self, iou_threshold=0.35, max_missed=7):
        self.tracks = []
        self.next_id = 1
        self.iou_threshold = iou_threshold
        self.max_missed = max_missed

    def update(self, result, frame_index, frame_path=None):
        box = result.get("bounding_box")
        plate = result.get("plate", "UNKNOWN")

        if not box or len(box) != 4:
            return False

        best_track = None
        best_iou = 0.0

        for track in self.tracks:
            if not track.active:
                continue

            score = iou(box, track.last_box)
            if score > best_iou and score >= self.iou_threshold:
                best_iou = score
                best_track = track

        matched = False

        if best_track:
            matched = best_track.update(box, result, frame_index, frame_path)
            best_track.missed = 0
        else:
            new_track = Track(
                track_id=self.next_id,
                box=box,
                plate=plate,
                result=result,
                frame_index=frame_index,
                frame_path=frame_path,
            )
            self.tracks.append(new_track)
            self.next_id += 1
            matched = True

        for track in self.tracks:
            if track.last_frame != frame_index:
                track.missed += 1
                if track.missed > self.max_missed:
                    track.active = False

        return matched

    def get_active_tracks(self):
        return [track for track in self.tracks if track.active or track.best_result]

    def get_final_tracks(self):
        return sorted(self.tracks, key=lambda t: (-t.hits, -t.best_score, t.track_id))
