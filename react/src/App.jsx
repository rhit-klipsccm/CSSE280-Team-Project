import { useState } from 'react'
import './App.css'

function App() {
  const [firstTime, changeFirstTime] = useState('');

  function adjustFirstTime(e) {
    changeFirstTime(e.target.value);
  }

  const [lastTime, changeLastTime] = useState('');

  function adjustLastTime(e) {
    changeLastTime(e.target.value);
  }

  function parseTime(time) {
    let timeString = time.split(":");
    let hours = parseFloat(timeString[0]);
    let minutes = parseFloat(timeString[1])/60;
    return hours + minutes;
  }

  //<> is a React Fragment that doesn't include extra DOM elements
  return (
      <>
        <h1 class="header">Calendar</h1>

        <div class = "register-form">
          <form method="POST" action="/requests" enctype="multipart/form-data" class="form">
          
            <p><input type="text" name="name" id="name" placeholder="Enter Reservation Name"
              title="Please enter a valid name" required/></p>

            <div class="time-container">
              <div class="labelgroup-container">
                <label for="date">Date:</label>
                <p><input type="date" name="date" id="date" required/></p>
              </div>

              <div class="labelgroup-container">
                <label for="start-time">Start Time:</label>
                <p><input type="time" name="start-time" id="start-time" value={firstTime} onChange={adjustFirstTime} required/></p>
              </div>
                
              <div class="labelgroup-container">
                <label for="end-time">End Time:</label>
                <p><input type="time" name="end-time" id="end-time" value={lastTime} onChange={adjustLastTime} required/></p>
              </div>
            </div>

            <p><input type="submit" name="submit-request" id="submit-request" value="Submit Reservation Request"
              onClick={async (e) => {
                let testFirstTime = parseTime(firstTime)
                let testLastTime = parseTime(lastTime)
                if (testLastTime <= testFirstTime)
                  testLastTime = testLastTime + 24;

                if (testLastTime - testFirstTime > 2) {
                  e.preventDefault()
                  alert("Message officer for times greater than 2 hours")
                  return false;
                }
                
                let options = {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    }
                }

                try {
                    let response = await fetch("requests", options)
                    if (!response.ok) {
                        throw new Error(`Response status: ${response.status}`);
                    }
                }
                catch (ex) {
                    console.error(ex);
                }
                //Prevent page reload
                return false;
              }}/>
            </p>
          </form>

          <iframe src="https://calendar.google.com/calendar/embed?src=357fce2b791dd6d8586930ba805fc98b311249542860748111772fc4bf67f4c8%40group.calendar.google.com&ctz=America%2FIndiana%2FIndianapolis" class="calendar"></iframe>
        </div>
      </>
  )
}

export default App
