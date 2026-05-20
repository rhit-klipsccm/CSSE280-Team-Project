import { useEffect, useState } from 'react'
import './Admin.css'

function Admin() {
  const [requests, setRequests] = useState([])
  const [selectedRequest, setSelectedRequest] = useState(null)
  const [approvalAction, setApprovalAction] = useState("Pending")
  const [reason, setReason] = useState("")
  const [description, setDescription] = useState("")

  useEffect(() => {
    fetch("/requests").then((response) => response.json()).then((data) => {
        // need to map the response object to an array, quicker to add to table below
        const requestArray = Object.entries(data).map(
          ([id, request]) => ({
            id,
            //https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax
            ...request
          })
        )
        setRequests(requestArray)
      })
  }, [])


  // TODO: clean this function up a little. works well but its kinda hodge-podged together.
  function submitApproval() {
    if (!selectedRequest) {
      alert("Please select a request first.")
      return
    }

    fetch(`/requests/${selectedRequest.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        action: approvalAction,
        reason: reason
      })

    }).then((response) => {
        if (!response.ok) {
          throw new Error("Failed to update request")
        }
        return response.text()

      }).then(() => {
        const updatedRequests = requests.map((request) => {
          if (request.id === selectedRequest.id) {
            return {
              ...request,
              approval: approvalAction,
              reason: reason
            }
          }
          return request
        })



        setRequests(updatedRequests)
        setSelectedRequest({
          ...selectedRequest,
          approval: approvalAction,
          reason: reason,
          description: description
        })

        alert("Request updated!")


      }).catch((error) => {
        console.error(error)
      })
  }


  // TODO: separate these two files so i can have my form script logic in one file, and the react page in this file
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  return (
    <>
      <h1 className="header">Admin Page</h1>

      <table className="request-table">
        <thead>
          <tr>
            <th>Request Name</th>
            <th>Request Date</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Approval Status</th>
          </tr>
        </thead>

        <tbody>
          {requests.map((request) => (
            <tr
              key={request.id}
              onClick={() => {
                setSelectedRequest(request)
                setApprovalAction(request.approval)
                setReason(request.reason || "")
                setDescription(request.description || "")
              }}

              className={ selectedRequest?.id === request.id ? "selected-row": "" } style={{ cursor: "pointer" }}>
              
              
              
              <td>{request.name}</td>
              <td>{request.date}</td>
              <td>{request.start_time}</td>
              <td>{request.end_time}</td>
              <td>{request.approval}</td>
            
            
            </tr>
          ))}
        </tbody>
      </table>

      <br />

      <div className="rightAlign">
        <h2>
          Selected request:{" "}
          {
            selectedRequest ? selectedRequest.name : "Select request from table"
          }
        </h2>

        <div className="approval-buttons">

          <label>
            <input
              type="radio"
              name="approval-status"
              value="Approved"
              checked={approvalAction === "Approved"}
              onChange={(e) => setApprovalAction(e.target.value)}
            />
            Approve
          </label>
          <label>
            <input
              type="radio"
              name="approval-status"
              value="Denied"
              checked={approvalAction === "Denied"}
              onChange={(e) => setApprovalAction(e.target.value)}
            />
            Deny
          </label>
          <label>
            <input
              type="radio"
              name="approval-status"
              value="Pending"
              checked={approvalAction === "Pending"}
              onChange={(e) => setApprovalAction(e.target.value)}
            />
            Pending
          </label>
        </div>
        <br/>

        <div className="textAreas">
          <div className="labelGroup">
            <label for="reason">
              Reason (optional):
            </label>
            <textarea
              name="reason"
              id="reason"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              rows="4"
              cols="50"/>
          </div>

          <div className="labelGroup">
            <label for="description">
              Description:
            </label>
            <textarea
              readOnly
              name="description"
              id="description"
              value={description}
              rows="4"
              cols="50"/>
          </div>
        </div>

        <button onClick={submitApproval}>
          Submit
        </button>
      </div>
    </>
  )
}

export default Admin