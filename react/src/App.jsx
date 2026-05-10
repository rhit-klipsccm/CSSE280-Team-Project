import { useState } from 'react'
import './App.css'

function App() {
  

  //<> is a React Fragment that doesn't include extra DOM elements
  return (
      <>
        <iframe src="https://calendar.google.com/calendar/embed?src=357fce2b791dd6d8586930ba805fc98b311249542860748111772fc4bf67f4c8%40group.calendar.google.com&ctz=America%2FIndiana%2FIndianapolis"></iframe>

        <form method="POST" action="/requests" enctype="application/x-www-form-urlencoded">
          
          <label for="name">Request Name:</label>
          <p><input type="text" name="name" id="name" placeholder="Enter seven words or less"/></p>

          <label for="date">Request Date:</label>
          <p><input type="text" name="date" id="date"/></p>

          <label for="start-time">Request Start Time:</label>
          <p><input type="text" name="start-time" id="start-time"/></p>
          
          <label for="end-time">Request End Time:</label>
          <p><input type="text" name="end-time" id="end-time"/></p>
        
        </form>
      </>
  )
}

export default App
