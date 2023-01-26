## how to use object tracker:
```zsh
from object_tracker.object_tracker import ObjectTracker
tracker = ObjectTracker("dimp", "dimp18")
tracker.init_bounding_box(frame, [x,y,w,h])
image, data = self.tracker.run_frame(frame)
image: raw image
data: [min_x, min_y, w, h, flag, score]
```
