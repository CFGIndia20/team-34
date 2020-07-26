## Code For Good
## Organisation - The Nudge Foundation
# Team - 34 Geeks for Social Change (GSC)
## Team Mentors - Saurin Tailor, Rahul Dhir
## Contact details of team members are : 

 - Team member 1 - Arun Vishwakarma, arunv8991@gmail.com

 - Team member 2 - Ayushi Desai, desaiayu@gmail.com

 - Team member 3 - Kunal Saraf, saraffkunal@gmail.com

 - Team member 4 - Monica B, monicayadhav@gmail.com

 - Team member 5 - Sahana K S, sahanaks1999@gmail.com

 - Team member 6 - Manan Doshi, manandoshi1607@gmail.com

## Problem Statement Description 
The foundation faces difficulty in distributing students to batches that run on the time slots preferred by students. Presently, the batch allocation is done as per the teacher's preference which sometimes leads to students dropping out of the course. Also, this entire process runs in manual mode. Hence, a fully automated solution is required which overcomes the downfalls of all such situations.

## Solution Proposed
 - Automated distribution of student in different batches.
 - Automated allotment of teachers to thier respective batches.
 - Dashboard for Admin - To trigger automated resource allocation and batch formation.
 - Dashboard for Teachers - To mark attendance, award scores, broadcast links and communicate with admin.
 - Dashboard for Students - To keep a track on their progress.
 - All users can view their daily schedule on the dashboard.
 - A separate placement portal to connect potential employees and employers.

## Technologies Used
 - Front-end - HTML, CSS, JavaScript, Bootstrap
 - Back-end - Flask
 - Database - MongoDb

<!-- <img src="assets/images/bracket_icon.png" alt="Bracket Chat Logo" width="200px" height="200px"> -->

## API End Points
### Admin Panel (Training Portal)
 - http://localhost:5000/admin/ - Provide the admin an option to trigger automatic batch allocation to students and to trigger automatic teacher allotment for batches
 - http://localhost:5000/admin/admin/students_allocation - It runs the algorithm in the background and groups students and displays the grouping via a table
 - http://localhost:5000/admin/admin/teachers_allocation - It runs the second algorithm in the background and allots teachers to batches and displays it in the form of a table

### Student Panel (Training Portal)
 - http://localhost:5000/students/analytics - To track progress and attendance
 - http://localhost:5000/students/schedule - To view daily schedule

### Teacher Panel (Training Portal)
 - http://localhost:5000/teachers/schedule - To get his/her schedule
 - http://localhost:5000/teacher_batches_attendance - To mark the attendance of students
 - http://localhost:5000/teacher_batches_marks - To assign marks to each student

### Admin Panel (Placement Portal)
 - http://localhost:5000/placement/employers - To get the list of all students in order of maximum score 

### Student Panel (Placement Portal)
 - http://localhost:5000/placement/candidate -To get the list of all the jobs sorted in descending order of salary


## Algorithms Developed
### Grouping of students to form batch
We are considering perferences of students for each slot. Based on that we look on the students who are already a part of those 4 slots, and out of the 4 choices the one which is least close to a multiple of 15 is the one where our current student is added in order to maintain equal batch sizes.

### Assigning batches to teacher
Algorithm picks all the batches in a round-robin fasion and pick up a teacher using random number generator in built python library. Once we have picked a teacher, we check for all the constraints provided to us, to name a few
 - No teacher should have consecutive classes
 - Every teacher should have one class daily
 - Span of classes for a teacher on a particular day should be restricted within a windows of maximum 8 hours
 
 ## Innovation and Features Implemented
  - Our app provides an intuitive way to view diifferent students, teachers and companies involved in the process.
  - We have tried to resolve problem of automated batch distribution so that it can work even with varying number of teachers and candidates.
  - With our app candidates can now make use of placement portal and view job listings, that helps them to be aware of all job opportunities.
  - Our app also allows employer to view students and filter them on basis of skillsets !
 
 ## Our journey
  - Problem statement selection
  - Brainstorming session, thourough discussions
  - Work distribution discussion, deadlines proposed
  - Started coding with implementing simple features like registration page
  - After few hours, all of us were familiar with the work and each of us knew what we have to do further
  - There were discussions at regular intervals to catch up with team mates, and to determine what has to be done next
  - Regular discussions helped us to collaborate better while working on different features
  - At the end we were able to produce a MVP for given problem statement
 
 ## How we have tried to make our app scalable
  - Web APIs have been developed, which can be used to develop mobile application later
  - The algorithm used could handle large number of candidates and implement a good batch distribution
  - Database used is MongoDB so it does support concurrency and any changes in data models
 
