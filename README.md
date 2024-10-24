# auto_driving
run auto_driving.py from cmd

sample test cases:
list of cars in a field of 10*10:
- A, (1,2) N, FFRFFFFRRL
- B, (7,8) W, FFLFFFFFFF
- C, (9,9) S, FFRFFFFRRL

result:
 - A, collides with B at (5,4) at step 7
 - B, collides with A at (5,4) at step 7
 - C, (5,7 ) N at step 10
