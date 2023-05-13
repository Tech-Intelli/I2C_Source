import React,{useState }from "react";
import "./Layout.css"
import {SignInModal} from "../SignInModal/SignInModal"

export const Layout = ()=>{
    const [show, setShow] = useState(false);
    const handleShow = () => setShow(true);
    const handleClose = () => setShow(false);

    return (
        <>
    <div>
        <div className="header">
            <div>
                <p>ExplAIstic</p>
            </div>
            <div className= "icons">
                <i className="fa-regular fa-user"></i>
                <i className="fa-solid fa-bars"></i>
            </div>
        </div>
        <section>
        <div className="content">
            <div className="innerContent">
                <p>Having tough time finding <span>Perfect Caption</span>?</p>
                <button className="btn-style" onClick={handleShow}>Start Now</button>
           </div>
        </div>
        <div className="footer">
        </div>
        </section>
        {show?<SignInModal show = {show} handleClose = {handleClose} handleShow = {handleShow} />:null}
        
    </div>
   
    </>
    )
}