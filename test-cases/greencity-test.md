ID: 1
<br>
Title: Testing searchbar using existing event
<br>
Precondition: on Events page, there is at least 1 event
<br>

| Step | Action | Data | Expected Result |
| :--- | :--- | :--- | :--- |
| 1 | Click on the searchbar | - | Searchbar becomes active for typing |
| 2 | Type in the name of an existing event | - | Events with these words in the name show up |

<br>
ID: 2
<br>
Title: Testing searchbar using non-existent event
<br>
Precondition: on Events page,there is at least 1 event

| Step | Action | Data | Expected Result |
| :--- | :--- | :--- | :--- |
| 1 | Click on the searchbar | - | Searchbar becomes active for typing |
| 2 | Type in the name of a non existing event | - | "No results match your search criteria" message shows up |

<br>
ID: 3
<br>
Title: Testing date filter
<br>
Precondition: on Events page

| Step | Action | Data | Expected Result |
| :--- | :--- | :--- | :--- |
| 1 | Click the "Date" filter button | - | Date picker shows up |
| 2 | Choose the lower bound date | "12.03.2025" | Chosen date becomes selected |
| 3 | Choose the upper bound date | "30.03.2025" | Only events within these boundaries show up. Date boundaries show up in Filters bar |
| 4 | Click the Cross button on date filter | - | Date filter disapears from Filters bar. All the events show up |
