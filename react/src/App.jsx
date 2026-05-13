import { useState } from 'react'
import './App.css'

function App() {
  

  //<> is a React Fragment that doesn't include extra DOM elements
  return (
      <>
        <h1 class="header">Calendar</h1>

        <div class = "register-form">
          <form method="POST" action="/requests" enctype="multipart/form-data" class="form">
          
            <p><input type="text" name="name" id="name" placeholder="Enter Reservation Name"/></p>

            <div class="time-container">
              <div class="labelgroup-container">
                <label for="date">Date:</label>
                <p><input type="date" name="date" id="date"/></p>
              </div>

              <div class="labelgroup-container">
                <label for="start-time">Start Time:</label>
                <p><input type="time" name="start-time" id="start-time"/></p>
              </div>
                
              <div class="labelgroup-container">
                <label for="end-time">End Time:</label>
                <p><input type="time" name="end-time" id="end-time"/></p>
              </div>
            </div>

            <p><input type="submit" name="submit-request" id="submit-request" value="Submit Reservation Request"
              onClick={async () => {
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
