# FotoPhrame

Raspberry Pi 4 Photo Frame

This should've been a simple project, I just want my photos shown on a 4K resolution display using a Raspberry Pi 4. But I wanted some fading animations between each photo, and it seems like it is too much math for the wimpy Pi CPU. The framerate during the fading animations was too slow.

The current implementation uses idle time to run another thread that renders each fading animation frame into a cache buffer. When the time comes to display the fading animation, the buffer is shown on the screen sequentially as fast as possible. This is still slow but works well enough.

If this thread did not finish in time, then the fading animation is done using Numpy integer division instead of PIL alpha blending, just to save on some of the floating point calculations.
