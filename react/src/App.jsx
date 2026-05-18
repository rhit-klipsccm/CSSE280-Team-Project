import { useState } from 'react'
import Requests from './Requests.jsx'
import Admin from './Admin.jsx'

function Page(props) {
    return (   
        <>
            { props.admin ? 
                <Admin />
            : 
                <Requests />
            }      
        </>
   );
}

function App() {
    return (
        <Page admin={false} />
    );
}

export default App