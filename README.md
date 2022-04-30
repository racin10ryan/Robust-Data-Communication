# Robust-Data-Communication
Progress: 	
	- Full control of radios with XMLRPC

Known Bugs: 		
	- Amplifications are not. Will have to figure them out and update

Bugs Fixed:
	- Missing length tag when Tx was stopped then started again
		FIX:Copy Block added and set to disable by default. Enable when
		file is loaded  
	- Hackrf One radio would freeze when it was assigned to be the Tx, 
	  the flowgraph was stopped, then started again.
		FIX: Updated HackRF firmware and libhackrf
	- Constellation did not change correctly
		FIX: When radio is stopped, the build/deconstruct packet functions
		are disconnected,regenerated, then connected
	- No transmission when setting the radio to 915 MHz
		FIX: The constant for 915MHz was incorrect. Changed constant from
		9.15e6 to 915e6
To Do: 
	- Implement packetizer
	- Implement ZMQ
	- Develope and implement decision algorithms (While there is a
	  function that selects frequency and constellation, it will need to be
	  updated to take strings from from the decision ["LOW", "MID", "HIGH]
	  ["BPSK","QPSK","16QAM"]) 
	- Fix Bugs
	- Remove Herobrine
		 
