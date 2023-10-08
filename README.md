# Photoshare

## ER (Entity-Relationship) Diagram
![image](https://github.com/lukkn/Photoshare/assets/70594133/f3746267-7d24-4074-b463-dbdc436d95c3)
**Figure 1** Entity-relationship (ER) diagram for the Photoshare database depicted using Chen’s notation.

## Relational Schema
### Schema description
This section describes the tables in the PhotoShare database by listing the following information for
each table:
- Column name
- Data type of each column
- Length of character columns
- Status of column detailing whether it is a primary or foreign key, whether it can take on null
values and whether a delete action cascades
- Description of the data to be entered into the column

**Table 1.** Users
| Column name | Data type | Length | Status | Description|
| ----------- | --------- | ------ | ------ | ---------- |
| User_id     | Integer   | 100    | Primary key, foreign key, not null, auto increment, on delete cascade | Unique nuber code for each registered user |
| Email       | Varchar   | 100    | Unique, not null | Unique email used for user registration and login |
| Password    | Varchar   | 100    | Not null | Password used for user login |
| First_Name  | Varchar   | 100    |          | User first name |
| Last_Name   | Varchar   | 100    |          | User last name |
| Gender      | Varchar   | 100    |          | User gender |
| Hometown    | Varchar   | 100    |          | User hometown |
| Birth_date  | Date      |        |          | User date of birth |

**Table 2.** Albums
| Column name | Data type | Length | Status | Description|
| ----------- | --------- | ------ | ------ | ---------- |
| Albums_id   | Integer   |        | Primary key, not null, auto increment | Unique number code for each album |
| User_id     | Integer   |        | Foreign key, not null, on delete cascade | User ID of user who owns the album |
| Name        | Varchar   | 100    |          | Name of album |
| Date        | Date      |        |          | Date on which the album was created |

**Table 3.** Tags
| Column name | Data type | Length | Status | Description|
| ----------- | --------- | ------ | ------ | ---------- |
| Photo_id    | Integer   | 100    | Primary key, not null, auto increment, on delete cascade | Photo ID of photo that the tag is attached to |
| Tag         | Varchar   | 100    | Primary key, not null | Tag name |

**Table 4.** Photos
| Column name | Data type | Length | Status | Description|
| ----------- | --------- | ------ | ------ | ---------- |
| Photo_id    | Integer   |        | Primary key, not null, auto increment | Unique number code for each photo |
| Albums_id   | Integer   |        | Foreign key, not null, on delete cascade | Album ID of album which contains the photo |
| User_id     | Integer   |        | Foreign key, not null | User ID of user who owns the album |
| Data        | Longblob  |        | | Data representing the actual image that was uploaded |
| Caption     | Varchar   | 100    | | Caption of photo |


**Table 5.** Friends
| Column name | Data type | Length | Status | Description|
| ----------- | --------- | ------ | ------ | ---------- |
| User_id1    | Integer   |        | Primary key, foreign key, not null | User ID of a user who is a friend with another user |
| User_id2    | Integer   |        | Primary key, foreign key, not null | User ID of a second user who is a friend with the first user  |
*ADDITIONAL CONSTRAINTS: UID1 and UID2 cannot be the same*


**Table 6.** Comments
| Column name | Data type | Length | Status | Description|
| ----------- | --------- | ------ | ------ | ---------- |
| Comment_id  | Integer   |        | Primary key, not null, auto increment | Unique nuber code for each comment |
| User_id     | Integer   |        | Foreign key, not null, on delete cascade | User ID of the user who commented on the photo |
| Photo_id    | Integer   |        | Foreign key, not null, on delete cascase | Photo ID of photo commented on by the user |
| Text        | Varchar   | 100    |          | Text content of the comment |

**Table 7.** Likes
| Column name | Data type | Length | Status | Description|
| ----------- | --------- | ------ | ------ | ---------- |
| User_id     | Integer   |        | Primary key, foreign key, not null, on delete cascade | User ID of the user who liked the photo |
| Photo_id    | Integer   |        | Primary key, foreign key, not null, on delete cascase | Photo ID of photo liked by the user |
