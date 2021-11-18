Hello! 

This little script asks for an input wikipedia URL and an integer value,
scraping the outgoing page links from the first paragraph of the input page,
and builds a network graph outwards as many degrees as requested.

I built this to learn some new skills,
and build a test case for visualizing interconnected documents. 

NB: This computation is inherently exponential, so please show restraint.
I'm sure excessive request would annoy the great team at Wikipedia as well.
At 3+ degrees of adjacency, the graph as it is becomes too cluttered.
I recommend playing around with the physics with the sliders provided.
I recommend:
	- forceAtlas2Based solver
	- reducing centralGravity (>0)
	- reducing gravitationalConstant
	- playing around!
If you find any optimal physics/other options, 
let me know or go ahead and build it.

This is just a working model,
and I'm sure the code can be refined with a bit more thought. 

wikigraph.html included is an example output, 
given the input URL https://en.wikipedia.org/wiki/Amphotericin_B 
and the adjacency factor 3.

