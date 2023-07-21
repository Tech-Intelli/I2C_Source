import React,{useState }from "react";
import "./Layout.css"
import {SignInModal} from "../SignInModal/SignInModal"
import Navbar from "../Navbar/Navbar";
import LandingPageImage from '../assets/images/landing-page-image-1.png';
export const Layout = ()=>{
    const [show, setShow] = useState(false);
    const handleShow = () => setShow(true);
    const handleClose = () => setShow(false);

    return (
        <>
    <div>
        {/* <Navbar flag={false}/> */}
        <section>
        <div className="content">
            <div className="innerContent">
                <div className="tagline">
                    <p className="title">CapGenAIze</p>
                    <p className="tag">Crafting Captions with AI Precision</p>
                </div>
                <button className="btn-style" onClick={handleShow}>Start Now</button>
           </div>
           <div className="images">
            <img src={LandingPageImage} alt="" />
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