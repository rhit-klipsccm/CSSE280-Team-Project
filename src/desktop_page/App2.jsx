import { useState } from 'react'

function App() {
  const [testguy, alterTestguy] = useState('desktopnow')

  function doSomething(e) {
    alterTestguy(e.target.value)
  }

  //<> is a React Fragment that doesn't include extra DOM elements
  return (
    <> 
      <h1>Shopping List</h1>
      <div>
        <form>
          <p>
            <input type="text" id="text1" required pattern="\w[0-9a-zA-Z\- ]*"
              title="Must have at least one non-whitespace character and no special characters."
              onChange={doSomething} value={doSomething}></input>
          </p>
          <p>
            <input id="button1" type="button" value="Add Item To List" 
              // TODO: With your instructor
            ></input>
          </p>
        </form>
      </div>
      <div className="list-container">
        <div className="list">
          <section name="to_get">
            <h2>To Get:</h2>
            <ul id="list1">{
              testguy
            }
            </ul>
          </section>
        </div>
        <div className="list">
          <section name="got">
            <h2>Got:</h2>
            <ul id="list2">{
              // TODO: With your instructor
            }
            </ul>
          </section>
        </div>
      </div>
    </>
  )
}

export default App
