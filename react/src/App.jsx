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
        changePageType(!pageType);
    }

    return (
        <>
            <Page admin={pageType} />
            <button onClick={swapPageType}>Swap</button>
        </>
    );
}

export default App