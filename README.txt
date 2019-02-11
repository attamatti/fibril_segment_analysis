version 1.2.1
20190211


analyses all crossover lengths and makes histogram.
also allows extraction of like crossovers as particle sets for 2d classification.

To use:
Works best of fibrils that have been computationally stratghtened.  
Use my make_bfil_parfile.py script and bsoft's bfil program to extract and computationally straighten each fibril.  
Make the extraction box width for the straightened fibril significantly larger than the maxium crossover length. 

The script can also be used on raw micrographs, but any curvature in the fibrils will reduce the accuracy of the results.
To pick a raw micrograph do the same thing clicking on an endpoint, each crossover in sequence, and a final endpoint.  
To start a new fibril on the same micrograph, click off of the image on the left side and then pick the next fibril.  

To use the program first pick every fibril.
Using e2boxer.py click on an endpoint, each crossover in order, and then a final endpoint for each fibril.  
Save the coordinates in e2boxer.py.  
Then run the script. Tell it '*.box' when it asks for input.

OTHER INCLUDED SCRIPTS:
- rln_match_ctf_to_straigntened.py writes a relion micrographs_ctf.star file for straightened fibrils -- see below
- datacheck-segment-analysis_MRC.py outputs a picture of each image with the actual fibrils picked drawn on it. 	
used for validating that you are actually picking what you think you are.

OUTPUTS:
-seg-analysis-relion.sh: a script that uses relion to extract each segment class as a particle stack for 2d classification in relion.
currently written for relion 2.1 - haven't checked if it's compatible with relion 3 yet... will get to that eventually/

run it with
seg-analysis-relion.sh <micrographs_ctf.star>

where <micrographs_ctf.star> is a starfile containing all of the ctf info from relion ctf determination.
If using straightened fibrils use the script rln_match_ctf_to_straigntened.py  (included) to write a micrographs_ctf.star file with the correct ctf info for each straightened fibril.

- seg-class.log: Exhaustive data dump.


DATA RESTRICTIONS
- current data limit 9,999 fibrils / 99,999 segments 
- NO dashes in filenames!!
- all images must be picked with same box size

TODO
- fix the problem where if the first picked point is too close to the edge the coordinates are negative becasue of the box size and the fibril is skipped.
get around this by using very small box size when picking.  

