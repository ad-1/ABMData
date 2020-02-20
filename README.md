# ABM Data Coding Challenge

## EDIFACT Message Parser

Taking an EDIFACT message text, parse out the all the LOC segments and populate an array with the 2nd and 3rd element of each segment. 
   
    Completed in Python and C#
    
## XML Parser

Given an xml document ('doc.xml'), extracting the RefText values for the following RefCodes: ‘MWB’, ‘TRV’ and ‘CAR’.

    Completed in Python
    
## Web Service

Webservice - respond with a status code which is based on parsing the contents of the XML payload ('payload.xml')

a.	If the XML document specified in payload is passed
            then return a status of ‘0’ – which means
            the document was structured correctly.
    
b.	If the Declararation’s Command <> ‘DEFAULT’
            then return ‘-1’ – which means invalid command specified.

c.	If the SiteID <> ‘DUB’ then return ‘-2’ – invalid Site specified.

    Completed in Python using Flask. 'POST' sent using Postman application.