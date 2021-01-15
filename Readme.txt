MODLIST ARRANGER


Modlist Arranger is a simple, universally-designed organizational tool. It can automatically gather information from Nexus URLs to create lists of categorized mods and display their details in a concise manner, with a host of other quality of life features. It is NOT a mod manager, and it will NOT install or download mods for you. It is simply a utility to create and save modlists.

If you're the type of person that likes to document the mods you use or want to keep an eye on, this might be something you'd like.


FEATURES


I've displayed some of the features in the screenshots, but if you'd like more detail, most of the important features will be listed below.
-Categorized Modlist Creation: Create modlists split into custom, renameable, and colorable categories, with no limit and for ANY game
-Automated Nexus Link Parsing: Automatically get the name, description, and game of to add to the modlist with a single URL copy-paste. Non-Nexus mods can still be inserted manually.
-Incompatibility Checking System: Automatically check for conflicts for mods that you've made an incompatibility list for with the rest of the mods in your list.
-Save and Load: Save and load modlists freely as .malist files
-Editable Mod Descriptions: Edit any mod's description at any time, to make personal notes or otherwise.
-Collapsable Categories: Collapse/expand each category to hide/show its mods by double clicking any category name, with options to also expand or collapse ALL categories.
-Quick URL Opening: Click the name of any mod to automatically open its linked URL in a browser, with options to open ALL links in a single category or in the entire modlist
-Toggleable Display: 2 separate views for mods: the default view and the more concise list view
-Filter Mods: Filter bar to search for specific mods in the list based on name.
-Extensive Removal Options: Options to remove single mods, selected mods, all mods in a category, or all mods in the modlist (leaving the categories empty)
-Per Category Index System: Separately numbered indices for mods in each of your categories.
-Total Mod Count: A tally for the total number of mods in the list shown at the bottom right of the app.
-An optional modlist file you can load up with empty categories that I personally use.


QUICK START


1) Extract the zip file anywhere, and keep the extracted files together
2) Run the program
3) You should see a new modlist with the "Mods" category placed in it. You may rename this category to  whatever you want or add new categories with right click.
4) Input a Nexus URL into the bar on top and click 'Add to End' to add that mod to the end of the list, or right click to insert a Nexus or non-Nexus mod URL at a specific place, or add a new category.
5) Click the button at the top left, the one directly left of the "Add to End" button, to switch between default and list view
6) Go nuts

﻿P.S. Loaded modlists will start with all categories collapsed by default. Just double-click a category name to expand it again. You may change this setting ﻿in the Edit Menu at the top-left.


HOTKEYS


-Right Click: Open a contextual drop-down menu with a wide variety of options to perform
-Ctrl+A: Select all mods (not categories) in the modlist
-Up and Down Arrow Keys: Move any selected mod(s) or mod category up or down.
-Ctrl+E: Scan for conflicts using your custom incompatibility lists for each mod.
-Ctrl+R: Clear the conflict highlights created after scanning for conflicts.
-Ctrl+N, Ctrl+O, Ctrl+S, Ctrl+Shift+S: Perform the New File, Open, Save, and Save As commands, respectively. 
-Ctrl+Q: Quit the program.
That's about it


IN-DEPTH HOW-TO


-URL Opening: Click on any mod's name to open its connected URL in your default browser. Use the right-click menu to open all URLs in a clicked category. Click on the Edit Menu in the top-left to open all mods in the entire modlist.
-Color Changing: Click on the 'Change Mod Color To...' option in the right-click menu to change the color of any mod's display to several preset colors.
-Multiple Selection: Click the index number of a mod to select it, and shift click after to select multiple in a row
-Drag-and-Drop: Click and hold an index number and drag it up or down to move any number of selected mods within a category. Mods can NOT be moved into other categories this way (was too lazy to figure that out)
-Moving Mods Between Categories: Use the arrow keys or the arrow buttons at the bottom to move selected categories or mods up or down. Mods CAN be moved into other categories this way. (Example: 4 mods selected together will all move out of the bottom of a category into the top of the next category at the same time if told to move down)
-Category Collapsing: Double-click to collapse categories (collapsed categories have a white indicator on the left). Double click collapsed categories to expand them.
-Description Editing: Click a mod's description to start editing it.
-Filtering: Enter text into the Filter bar to show only mods with that text in their names
-Incompatibility Insertion: Click on the Incompatibility Manager option in the right-click-menu. You may view, add, and remove URLs for mods you've determined to be incompatible with this mod in this window. Click 'Add' to start the automatic link-grabbing.
-Incompatibility Scanning: Open the Edit Menu on the top-left and choose 'Check For All Incompatibilities' to scan the list for all mods that conflict using your manually-inserted incompatibility lists. This will highlight all conflicting mods and display their conflicts in the right-click menu.
-Starting Collapsed: Open the Edit Menu on the top-left and choose the bottom option to enable or disable whether all categories start collapsed (hidden) when loading a pre-existing modlist or not.
-Non-Nexus Insertion: When inserting a custom mod, only the URL and name entries are required. The other two are optional and can be left blank.
.malist Drag-and-Drop Loading: You can drag and drop .malist files onto the program to load that modlist quickly


KNOWN ISSUES


-Will update this section as bugs are discovered.
-NOTE: When inserting a Nexus URL, the mod might take a second to appear on the modlist because the Nexus' server is slow. Nothing I can really do about that, sorry, but you can just let it run for the second it takes to load and look for other mods in the meantime. This also means that using the batch nexus mod insertion system may take a long time depending on how many links were inserted.
-Automatically obtained descriptions will be cut-off if they are too long. This is because long descriptions are cut-off in the Nexus HTML files themselves, so I can't do much about it on my end.
-If ANYTHING goes wrong within the program (unlikely, but possible), the save-on-quit command won't work any more for that session. Normal saving should still function normally, but you won't get an error message if anything screws up, so just remember to save often.
-WARNING: A select few antivirus programs (including Microsoft's) seem to think of the exe for my application as a virus. This is a seemingly common issue for Python scripts compiled like mine is (through pyinstaller). I've rebuilt the application now, and have reduced the number of false positives significantly, but some antiviruses still flag it, as can be seen on VirusTotal﻿. I can pretty safely say to ignore these detections, but if you're still worried, that's fair. For even further clarity though, I have posted the github repository for my program here﻿, where you can see all the source files and code.
TLDR; THE PROGRAM IS SAFE. IGNORE ANTIVIRUS FALSE POSITIVES ON THIS PROGRAM.


QUESTIONS:


Q: Are you going to add more features to this?
A: Nah, I'm pretty much done on features. I'll still poke around for bugs every now and then if they're not too annoying, but otherwise, the program is at exactly where I want it to be, and that's good enough for me. HOWEVER, if there are any suggestions that I find useful enough, I might look into implementing them.

Q: Are you going to improve the looks of the program?
A: What, you don't like the look? Or the royalty free desktop icon? Well tough luck. They're not changing unless someone wants to do it for me. And hey, at least it's better than what I could do in college.

Q: Will you add automatic URL mod insertion for sites besides Nexus?
A: If I find that I use mods from that site enough, sure, I could try. Most likely not though, since I get most of my mods from the Nexus.

Q: Can I post this tool on ____ site or ____ forum?
A: If you want to link people to this page, feel free. If you want to redistribute this mod on other sites, you can do that too, as long as you give me proper credits and/or provide a link back to this page.