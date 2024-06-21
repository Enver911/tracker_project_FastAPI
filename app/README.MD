<h4> Beta version of task manager on Fast API. </h4> <br>

deploy commands in project directory: <br>
<h5>
    docker build -t tracker_fastapi_image . <br>
    docker run -d --name tracker -p 80:80 tracker_fastapi <br>
</h5>