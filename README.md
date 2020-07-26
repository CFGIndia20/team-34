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
 - http://localhost:5000/admin/view_batches - List 
 - http://localhost:5000/admin/view_batches
 - http://localhost:5000/admin/view_batches

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

For ppt - Archetecture, USP, Roadmap, Scalability

## Algorithms Developed
### Grouping of students to form batch - 
### Assigning batches to teacher
We pick all the batches in a round-robin fasion and pick up a teacher randomly using random number generator in built python library. Once we have picked a teacher, we check for all the constraints provided to us, to name a few
 - No teacher should have consecutive classes
 - Every teacher should have one class daily
 - Span of classes for a teacher on a particular day should be restrc