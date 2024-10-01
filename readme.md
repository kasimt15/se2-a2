Here are my cli commands:

flask init - This would initalize the datebase dropping all data from before (no agruments)

flask user create - This would allow for users who wish to apply to jobs to create an account that is associated with an id
Eg flask user create john_Doe pass john_Doe@gmail.com 1868-123-4567

flask job create - This allows for persons to post jobs 
Eg flask job create software_engineering build_software tech_company

flask job list - This allows for all the jobs that were posted to be displayed (no agruments)

flask application apply - This allows for a user to apply to a job, the user must use their id and the id of the job that they wish to apply to.
Eg flask application apply 2 1 (where 2 is the user id and 1 is the job id)

flask application list - This displays all the users who applied to a particular job, the id for the job must be used.
Eg flask application list 1 (where 1 is the job id)


