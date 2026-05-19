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
    const [pageType, changePageType] = useState(false);

    function swapPageType() {
        let password = "";
        if (!pageType)
            password = prompt("Input Admin Password");

        //You could probably make this better by drawing from a constant
        if (password === "Admin Key" || pageType)
            changePageType(!pageType);
    }

    return (
        <>
            <Page admin={pageType} />
            <p><button onClick={swapPageType}>Swap</button></p>
        </>
    );
}

export default App