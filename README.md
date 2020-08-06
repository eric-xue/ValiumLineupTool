# Valium Lineup Tool
Simple tool for fast lineup lookups. 

**NOTE:** Lineup images must be in .jpg format

## Todo

- Add space for text box and images relating to character specific info
    - ie: Sova charge + bounce amount
    
- Implement resolution scaling

- Create tool for user creation of lineup locations without touching xml config

- Seperate parts into seperate class for less bloated main func

## Updates
### 6/18
> **Changes**
>- Added xml file for usage in multiple images per lineup
>- Modified how certain pathnames were defined
>- Xml used to create spot names instead of from image filename to allow multiple images
### 6/19
> **Changes**
>- Added multiple images per lineup
>- Lists of agent, map, side now initialized with xml file
>- Removed reliance on .jpg format for lineup images through xml config 
>- Added some Sova lineups for attacker Haven
>- Removed usage of **glob** library to populate spot list and replaced w/ xml config 
>
> **Bugs**
>- Occasionally, when switching to new lineup, may have to press next twice in order to go to next image. 
>Believe this is related to current_picture. May have been fixed.  
### 7/15
> **Changes**
>- Added image resizing to reduce load time if large file such as 5mb image used. 
>- Added multiprocessing so resizing & main program can run at same time.
### 7/31
> **Changes**
>- Added menu bar with option to edit xml.
>- Edit option allows user to add and remove images without having to directly interact with the xml file itself.
>(Currently, user must input image name. Method to know which files you can add/remove will be added.)
>
> **To do**
>- Implement inheritance for the remove and add windows as large part of the code is exact same.
### 8/6
> **Changes**
>- Implemented better xml editing for adding and removing pictures.
>>**ADD**: User only allowed to add pictures that are not already part of the xml ie. no duplicate pictures.
>>
>>**REMOVE**: User only allowed to remove pictures that are part of the xml ie. can't input invalid name