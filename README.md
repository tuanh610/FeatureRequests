# FeatureRequests
HackerTrail assignment

The current release includes: 
1. Submit new request 
2. View all requests
3. View specific request 
4. Edit specific request 
5. Delete specific request 

Tech stack:
1. Core: Python, Django
2. Database: Django built-in data base (sqlite3)
3. Style: Materialize, cripsy-form

Logic on priority: 
1. 1 is highest priority
2. There is no maximum on priority 
Eg. you can have request of priority 1, 2 and 1000 of same client (the client says that 3rd one will be the last one they do)
3. If you submit 1 request with the same priority number with the an existing request (same client), 
then the existing will be pushed back to lower priority until there is no overlapping of priority
Eg. (1,2,3,4) -> Insert with priority 2 -> (1, 2(New Item), 3(Old:2), 4(Old:3), 5(Old:4)
    (1,2,3,5) -> Insert with priority 2 -> (1, 2(New Item), 3(Old:2), 4(Old:3), 5 (No change)
4. If a request is deleted then the priority list will not be updated. There will be just an empty slot there (like 1,2,3,5 if 4 is deleted)
5. If an item is edited and the prioriy changes then it will go thorugh the 3rd point

Edit/Update is done with post request so that you cannot refresh and redo it and also not able to just type it in the address bar.

Edit/Update only available if you have login with admin password

Admin username: admin 

Admin password: test1993
