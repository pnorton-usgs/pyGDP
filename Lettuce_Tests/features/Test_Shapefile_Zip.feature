Feature: Zipping up shapefiles
	In order to make sure all the parts of a shapefile zip correctly
	As a person who tends to break everything unintentionally
	We will make sure that those files get zipped and uploaded successfully
		
	Scenario: Upload zip file
		Given I have a test shapefile and all its associated components
		When I run the shapeToZip function
		And I upload the shapefile
		I get back the shapefile name that I expect