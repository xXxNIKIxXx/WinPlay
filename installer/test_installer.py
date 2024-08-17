import webview
import tkinter as tk
from tkinter import filedialog

global window
window = None

def select_folder():
    root = tk.Tk()
    root.withdraw()

    directory_path = filedialog.askdirectory(mustexist=False, title="Enter installation directory", initialdir="C:\\")

    root.destroy()

    return directory_path

def click_handler(e):
    if e.get("target").get("innerHTML") == "Cancel":
        global window
        window.destroy()
    elif e.get("target").get("innerHTML") == "Finish":
        window.destroy()
    elif e.get("target").get("id") == "installPath":
        file_loc = select_folder()
        window.evaluate_js('document.querySelector("#installPath").value = "' + file_loc +'"')
        window.evaluate_js('document.getElementById("next").disabled = false')
        print(file_loc)

def bind(window):
    install_button = window.dom.get_element('#next')
    ignore_button = window.dom.get_element('#cancle')
    path_button = window.dom.get_element('#installPath')

    install_button.events.click += click_handler
    ignore_button.events.click += click_handler
    path_button.events.click += click_handler

def window_c():
    global window
    window = webview.create_window(
            'Reboot', 
            html="""

<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<title>Web Installer</title>
</head>
<body>

<div id="installer">
    <div class="wrapper">
    <div class="row max_height no_margin">
        <div class="col-3 no_padding">
            <img class="fit" src="https://i.pinimg.com/736x/b4/d3/19/b4d319caa644f3912c03a4865a2fe940.jpg"/>
        </div>
        <div class="col no_padding">

            
    <div class="step active" id="step1">
        <h2>Welcome to the Web Installer</h2>
        <p>This is a simulated installation process.</p>
    </div>
    <div class="step" id="step2">
        <h2>Select Installation Location</h2>
        <input type="button" class="btn btn-info no_margin" id="installPath" placeholder="Enter installation path..." value="Enter installation path...">
    </div>
    <div class="step" id="step3">
        <h2>Installing...</h2>
        <p>Please wait while the installation is in progress...</p>
        <div class="progress-container">
            <div id="progressBar" class="progress-bar"></div>
        </div>
    </div>
    <div class="step" id="step4">
        <h2>Done!</h2>
        <p>The installation was successful.</p>
    </div>

        </div>
    </div>
    </div>
    <div class="row button_row no_margin">
        <div class="d-grid gap-2 d-md-flex justify-content-md-end no_margin">
            <button type="button" class="btn btn-secondary no_margin" id="back" onclick="prevStep()" disabled>Back</button>
            <button type="button" class="btn btn-primary no_margin" id="next" onclick="nextStep()">Next</button>
            <button type="button" class="btn btn-danger no_margin" id="cancle">Cancel</button>
        </div>
    </div>

</div>

</body>

<script>
    var current_step = 1;

    function nextStep() {
        if ((current_step + 1) == 5) {
            window.location.reload();
        }
        document.querySelector('.active').classList.remove('active');
        document.getElementById('step' + (current_step + 1)).classList.add('active');
        current_step++;
        check_back_button();
        check_next_button();

    }
    
    function prevStep() {
        document.querySelector('.active').classList.remove('active');
        document.getElementById('step' + (current_step - 1)).classList.add('active');
        current_step--;
        check_back_button();
        check_next_button();
    }

    function check_back_button() {
        if(current_step == 1) {
            document.querySelector('#back').disabled = true;
        } else {
            document.querySelector('#back').disabled = false;
        }
    }

    function check_next_button() {
        if(current_step == 2) {
            document.querySelector('#next').disabled = true;
            document.querySelector('#next').textContent = "Next";
            document.querySelector('#next').onclick = nextStep;
        } else if(current_step == 3) {
            document.querySelector('#next').textContent = "Install";
            document.querySelector('#next').onclick = startInstallation;
        } else if(current_step == 4) {
            document.querySelector('#next').textContent = "Finish";
            document.querySelector('#next').onclick = nextStep;
        } else {
            document.querySelector('#next').disabled = false;
            document.querySelector('#next').textContent = "Next";
            document.querySelector('#next').onclick = nextStep;
        }
    }
    
    function startInstallation() {
        document.getElementById('next').disabled = true; // Disable install button
        document.getElementById('back').disabled = true; // Optionally disable back button
        document.getElementById('cancle').disabled = true; // Optionally disable back button
        var progressBar = document.getElementById('progressBar');
        var width = 0;
        var interval = setInterval(function() {
            if(width >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    nextStep();
                    document.getElementById('next').disabled = false; // Disable install button
                    document.getElementById('back').disabled = false; // Optionally disable back button
                    document.getElementById('cancle').disabled = false; // Optionally disable back button
                }, 50); // Short delay before moving to the next step
            } else {
                width = width + 0.1;
                progressBar.style.width = width + '%';
            }
        }, 5); // Adjust speed here
    }
</script>

<style>
    body {
        font-family: Arial, sans-serif;
        margin: 0px;
        
    }
    

    .step {
        display: none;
    }
    
    .step.active {
        display: block;
        margin: 10px;
    }
    
    button {
        margin-top: 10px;
    }
    
    .progress-container {
        background-color: #eee;
    }
    
    .progress-bar {
        height: 20px;
        width: 0;
        background-color: #4CAF50;
    }

    .wrapper {
        height: calc(100vh - 78px);
    }

    .no_margin {
        margin: 0px;
        --bs-gutter-x: 0px;
    }

    .no_padding {
        padding: 0px;
    }

    .button_row {
        padding: 20px;
        background-color: #b9b9b9;
    }

    .max_height {
        height: 100%;
    }

    .fit {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
</style>

</html>

            """, draggable=False, resizable=False, frameless=True
        )

    webview.start(bind, window)
    
window_c()