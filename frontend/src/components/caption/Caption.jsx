import React, {useState} from 'react'
import "./Caption.css";
import Card from './Post/Card';
import { useLocation, useNavigate } from 'react-router-dom';
import Typed from 'typed.js';
import axios from 'axios';


const Caption = () => {
    const el = React.useRef(null);
    //Type Animation
    React.useEffect(() => {
        const typed = new Typed(el.current, {
          strings: [state.caption],
          typeSpeed: 5,
        });
    
        return () => {
          // Destroy Typed instance during cleanup to stop animation
          typed.destroy();
        };
      }, []);

    const navigate = useNavigate();
    const { state } = useLocation();
    const handleReupload = () => {
        navigate('/uploadfile') ;// Go back two pages
      };
    
    const handleRegenerate = () => {
        navigate('/generatecaption'); // Should only go back 1 page
    };
    const handleShare = () => {
        console.log("Share");
        //Logic for Implementing the Share Button
    };

    //Implementing Logout Feature
    const [showDropdown, setShowDropdown] = useState(false); // To convert the user icon into dropdown
    const toggleDropdown = () => {
        console.log("User was clicked");
        setShowDropdown(!showDropdown);
    };
    const handleLogout = async() => {
        await axios.post("http://localhost:9000/logout_user")
        .then((res)=>{
        navigate("/");
        })
        .catch((err) => {
        console.log("Error", err);
        });
        console.log("Go to Login")
    };

  return (

    <>
    <div>
        <div className="header-page3">
            <div>
                <p>ExplAIstic</p>
            </div>
            <div className= "icons-page3">
            <i
                className={`fa-regular fa-user ${showDropdown ? 'active' : ''}`}
                onClick={toggleDropdown}
              ></i>
                <i className="fa-solid fa-bars"></i>
            </div>
        </div>
        <section>
        <div className="content-page3">
            {showDropdown && (
                <div className="dropdown-input">
                <ul>
                    <li onClick={handleLogout}>Log out</li>
                </ul>
                </div>
            )}
            <div className="innerContent-page3">
                <div className='innerContent-div'> 
                    <div className='text' >
                        <p className="steps-page3" >Step 3 :Share Your Caption</p>
                        <div className='generated-caption'>
                            <textarea style={{resize:"none"}}className='caption' ref={el}></textarea>
                        </div>
                        <div className="utilities">
                            <button className='btn-reupload' onClick={handleReupload}>Reupload <i class="fa-solid fa-cloud-arrow-up"></i></button>
                            <button className='btn-regenerate' onClick={handleRegenerate} >Regenerate <i class="fa-solid fa-arrows-rotate"></i></button>
                        </div>
                    </div>
                    <div>
                        <Card path={state.file_path} />
                    </div>
                </div>
                <button className='btn-style-page3' onClick={handleShare}>Share</button>
                
           </div>
           

        </div>
        <div className="footer-page3">
        </div>
        </section>

        <div className='images page3'>
            
        </div>
        
        
    </div>
   
    </>
  )
       
   
   

}

export default Caption