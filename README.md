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


## Design Description
### Design Justification
a. Photos is a weak entity identified by the album which contains it, ensuring that photos are deleted when the album they belong to is deleted.
b. Users are categorized into registered and guest users as guest users can only browse and comment on photos. Guest users cannot like photos, as all guests are assigned a default username, and the site displays who liked each photo. This would lead to many entries indicating a guest liked the photo, without the ability to distinguish between the guest users. Registered users can own albums, and have more data associated with them such as first and last name etc.
c. Comments and Likes are designed to deleted when the owner of the comments or likes are deleted. Users cannot be deleted under the current implementation, but future iterations of the site may support user deletion.
d. The schema inserts a default guest user, which is used to identify guest comments as such. The guest account is not made to be logged in to and is only used for its user_id value of 1, which is assigned to the comments any guest user makes.
e. Comments, likes and photos display their owners as email addresses instead of name, as the name information is optional for any user who creates an account.
f. The upload feature is only available within an album, this ensures that all photos belong to an album as they are uploaded.
g. Users can search photos by tags in the “Browse” page, which returns any photo with matching tags from ALL photos. Searching by tags is also available in the “View my Albums” page, which only returns photos with matching tags from the USER’s photos.

## Design Limitations
a. Recommendations will not be available to a user until they have used at least five tags
b. Tags must be added as part of the photo uploading process, tags cannot be added after a photo has been uploaded.
c. Users can log into the default guest account if they gain access to the password, which would allow them to use all the features of the site.
d. The site assumes that a single user will not have two or more albums with the same name.
e. The site does not support backwards navigation of pages outside of the back button of the browser.
f. The user can only upload one photo at once
g. Users cannot change their email and password

## Site Structure
### Landing
![image](https://github.com/lukkn/Photoshare/assets/70594133/ac788847-6821-4116-9a9e-47aa901072c2)

**Figure 2.** Default Landing Page
The default landing page directs users to:
1. Login
- Users will be redirected to the [login page](#login)
2. Create an account
- Users will be redirected to the [registration page](#register)
3. Continue as guest
- Users will be redirected to the [browse page](#browse)

### Authentication
#### Login
![image](https://github.com/lukkn/Photoshare/assets/70594133/197a77bb-2bb6-4412-9e73-41708d8e1825)

**Figure 3.** Login Page
The login page requests the user’s email and password, submitting may result in:
1. Successful login
- Users will be redirected to the [home page](#home)
2. Failure to login
- Users will be redirected to the [login retry page](#login-retry)

#### Register
![image](https://github.com/lukkn/Photoshare/assets/70594133/85a37213-3127-44be-ab58-266a406e5f2f)

**Figure 4.** Registration Page
The registration page requests the user to input an email and password, submitting may result in two possible scenarios:
1. An account with the same email already exists
- The user will be redirected to the [registration retry page](#registration-retry)
2. No account exists with the current email
- The user will be redirected to the [home page](#home)

### Retry
#### Login retry
![image](https://github.com/lukkn/Photoshare/assets/70594133/fadaf13e-3001-432b-81b5-9ccc93ff3438)

**Figure 5.** Login retry page
1. Try Again
- The user will be redirected to the [login page](#login)
2. Make an account
- The user will be redirected to the [registration page](#register)
  
#### Registration retry
![image](https://github.com/lukkn/Photoshare/assets/70594133/f14c6c79-df76-4708-a05e-65cdebb8e252)

**Figure 6.** Registration retry page
The user can reattempt registration user a valid email address. The page offers the same functions as the [registration page](#register). If the user clicks login, they will be redirected to the [login page](#login).

### Home
![image](https://github.com/lukkn/Photoshare/assets/70594133/50ae9685-821b-4a1d-b5fc-41c9be430c53)
![image](https://github.com/lukkn/Photoshare/assets/70594133/7af4a2ab-8155-4922-9de6-6a14e80dd505)
![image](https://github.com/lukkn/Photoshare/assets/70594133/8b476355-e5ff-49d9-ab90-64e868555fa7)

**Figure 7.** Variations of the home page
Variations of the home page exists, where the only difference is the message displayed at the top of the page. If redirected from the login page, it will display “Login successful!” If redirected from the registration page, it will display “Account Created!!” If redirected from any other page there will be no message.
The welcome message appears at the top of the page, under the optional message if there is any. It displays “Hello {user email}!”
The following links are available on the home page:
1. Browse
- The user will be redirected to the [browse page](#browse)
2. View Albums
- The user will be redirected to the [albums page](#view-all-albums)
3. Search Comments
- The user will be redirected to the [search comments page](#search-comments)
4. Profile
- The user will be redirected to the [profile page](#profile-information)
5. Friend list
- The user will be redirected to the [friends page](#friend-list)
6. Logout
- The user will remain on the home page, with the message “Logged out” displayed
7. You may also like
- The user will be redirected to the [recommendations page](#recommendations)

#### Top Users
The home page displays Top Users, which are ranked by their contribution score, which is calculated as the total amount of photos the user has uploaded plus the total amount of comments the user has made. At most 10 users are displayed at once. The ranking is refreshed along with the page.

#### Top Tags
The home page displays Top Tags, which are the most commonly used tags across the site. Score is calculated as the number of times the tag has been used.

### Browse
![image](https://github.com/lukkn/Photoshare/assets/70594133/67c43f9b-d999-47b8-a511-41ce1ec50cbd)

**Figure 8.** Browse page
The browse page displays all photos from the website, in the order of date uploaded. The user can either:
1. Search all photos by tags
- The user will need to enter the tags they wish to search by, separated by spaces. For example, the user may type in “small drone,” to which the system will respond by searching for photos with the tags “small” or “drone” or both.
- After clicking the search button, the user will be redirected to the [search tags page](#search-tags)
2. Click on a photo
- The user will be redirected to a [photo page](#photo)

### Albums
#### View all albums
![image](https://github.com/lukkn/Photoshare/assets/70594133/ecfac098-8158-43cc-85e5-991eb19542cd)

**Figure 9.** Albums page
The view albums page displays all the user’s albums, in ascending order of date of creation. The user may choose:
1. Search photos by tags
- The user will be redirected to the [search tags page](#search-tags)
2. Create a new album
- The user will be redirected to the [create album page](#create-album)
3. Home
- The user will be redirected to the [home page](#home)

#### View contents of one album
![image](https://github.com/lukkn/Photoshare/assets/70594133/de13d344-64a3-4727-ac81-90fb7521fead)

**Figure 10.** Album content page
The album page displays the name of the album currently being view on the top of the page and all photos within the album, along with their captions. The user may choose:
1. Delete album
- The album, along with all pictures within the album, will be deleted, and the user wil be redirected to the [albums page](#view-all-albums)
2. Upload a photo
- The user will be redirected to the [upload photo page](#upload-photo-to-album)
3. Back to all albums
- The user will be redirected to the [albums page](#view-all-albums)
4. Home
- The user will be redirected to the [home page](#home)

#### Create Album
![image](https://github.com/lukkn/Photoshare/assets/70594133/5b86ba98-d6f6-4106-bd41-10726b7b5df0)

**Figure 11.** Create album page 
The create album page requests the user enter an album name. The system assumes that users enter a unique album name for each album created. Once the user clicks the create button, the album is created, and the user is redirected to the [albums page](#view-all-albums).

#### Upload photo to Album
![image](https://github.com/lukkn/Photoshare/assets/70594133/442cb516-7f4a-4775-833e-a9f5cc495c30)

**Figure 12.** Upload photo page
The upload photo page requests the user to choose an image file to upload from their local machine, and a caption to go with the photo. The users may choose:
1. Upload
- The photo will be uploaded, and the user will be redirected to the add tags page:
![image](https://github.com/lukkn/Photoshare/assets/70594133/41d6fd1f-5f82-443d-b18f-98d9631236cb)

**Figure 13.** Add tags page
The add tags page requests users to enter tags for the photo that was just uploaded. The required format is “#tag1#tag2” with no spaces, where each tag is separated by a hashtag symbol. Tags are not required, but the user may add as many tags as they wish. Once the user clicks the add tags button, the tags will be added to the photo and the user will be redirected to the corresponding photo page
2. Create new album
- The user will be redirected to the [create album page](#create-album)
3. Home
- The user will be redirected to the [home page](#home)

### Search
#### Search comments
![image](https://github.com/lukkn/Photoshare/assets/70594133/a8a11d4e-d7ed-4b2f-a2d2-aad6c6db5334)

**Figure 14.** Search comments page
The search comments page requests a string of text that the user wishes to search for amongst all the comments on the site. Once the user clicks the search button, the page will display all users that made comments that match the user’s input EXACTLY, and the number of times each user made that comment:
![image](https://github.com/lukkn/Photoshare/assets/70594133/1f9c5f0c-ae7c-46e0-b0bb-e0967c3efbaf)

**Figure 15.** Search for comment "Nice!"

#### Search Tags
![image](https://github.com/lukkn/Photoshare/assets/70594133/04d1ed6c-3263-48da-9637-77c91be9388c)

**Figure 16.** Search tags page
The search tags page displays all photos that have at least one tag matching the search terms. Each word (separated by a space) is considered one tag. Photos that have more matching tags will be displayed first. If two photos have the same number tags matching the search terms, the photo with less unrelated tags will be displayed first. 

### Photo
![image](https://github.com/lukkn/Photoshare/assets/70594133/d80a708a-3a18-46fa-91d6-afd3b75f3886)

**Figure 17.** A photo page
The photo page displays the photo that was clicked on, along with its caption and the user who uploaded the photo. The page also displays the tags associated with the photo, each tag is a clickable link, and will redirect users to the [search tags page](#search-tags) when clicked. Users may choose to:
1. Like
- The user will remain on the photo page, and the number of likes displayed will increment.
2. Comment
- The users will remain on the photo page, and their comment will appear on the page 
Comments that were made on the photo are also displayed. The number of likes the photo has received is also displayed, and is a clickable link. When clicked, the link will redirect users to the likes page:
![image](https://github.com/lukkn/Photoshare/assets/70594133/023ee7a0-987f-4fbe-bc94-b8e3d6c153ee)

**Figure 18.** Likes page
The likes page displays the email addresses of users who liked the corresponding photos.

### Profile
#### Profile Information
![image](https://github.com/lukkn/Photoshare/assets/70594133/3fe6e0d6-9f0c-4924-9e2b-8b4c9abe1061)

**Figure 19.** Profile page
The profile page displays the user’s information, users may click on the edit button which will redirect them to the edit [profile page](#edit-profile)

#### Edit Profile
![image](https://github.com/lukkn/Photoshare/assets/70594133/9df99721-8a41-41b8-a385-afd02310f5fa)

**Figure 20.** Edit Profile Page
The edit profile page requests inputs from the users about their info. Inputs are not required for all fields to submit. Once the user clicks the apply button they are redirected to the [profile page](#profile-information) with the changes applied.


###Friends
#### Friend List
![image](https://github.com/lukkn/Photoshare/assets/70594133/171e45b8-d4bf-4057-aa12-b9f3bf8a9c41)

**Figure 21.** Friends Page
The friends page displays all the user’s friends. The user may click on “add friends” which will redirect them to the [add friends page](#add-friends)

#### Add Friends
![image](https://github.com/lukkn/Photoshare/assets/70594133/49dc42f5-5647-4151-aac9-c7bd08428f29)

**Figure 22.** Add friends page
The add friends page allows users to add new friends. Recommended users are displayed, which are the friends of the user’s friends. The more a user appears in the user’s friends of friends list, the higher they rank on the recommendation. A comprehensive list of all users is also displayed.


### Recommendations
The recommendations page will display recommended photos if the user has used at least five tags:
![image](https://github.com/lukkn/Photoshare/assets/70594133/bddc39f9-4e4e-4050-a8ab-bedb26318c5e)

**Figure 23.** Recommended photos

If not, the page displays:
![image](https://github.com/lukkn/Photoshare/assets/70594133/e0649ff7-7efb-497c-842b-6950e133f78b)

**Figure 24.** Not enough tags for recommendation










