import React, { useState } from 'react'
import "./ChooseCaption.css"
import { useNavigate, useLocation } from 'react-router-dom';
import axios from "axios"
import { Circles } from "react-loader-spinner";
import facebook from "../assets/icons/facebook.svg";
import instagram from "../assets/icons/instagram.svg";
import twitter from "../assets/icons/twitter.svg";
import linkedin from "../assets/icons/linkedin.svg";

const ChooseCaption = () => {
    const location = useLocation()
    const token = localStorage.getItem('token')
    const [targetId, settargetId] = useState();
    const [selectSizeId,setSelectsizeId] = useState();
    const [platformId, setplatformId] = useState();
    const [tone,setTone]=useState("Casual");
    const [caption,setcaption] =useState("");
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [hashtag, setHashtag] = useState(0); // Number of hashtags
    const addBorder = {
        border:"2px solid #1C4042",
        borderRadius:"5px"
    }
    const bordernone = {
        border:"none",
    }


    const selectdiv = {
        background :"#1C4042",
        color : "#fff"
    }
    const styles = {
        background :"#fff",
        color:"#1C4042",
    }

    const handleChange = (id)=>{
        settargetId(id);
    }

    const handleSize = (id)=>{
        setSelectsizeId(id);
    }
    const handleFacebook = (id)=>{
        setplatformId(id);
    }

    const handleTwitter= (id)=>{
        setplatformId(id);
    }
    const handleInstagram = (id)=>{
        setplatformId(id);
    }
    const handleLinkedIn = (id)=>{
        setplatformId(id);
    }
    const generateCaption = () =>{
        setLoading(true);
        const context= location?.state?.memory || ''; //Setting the context as the memory that the user provides. If the user does not provide any value, the context is set to ''. 
        
        axios.get(`http://localhost:9000/generate_image_video_caption?caption_size=${selectSizeId}&context=${context}&style=${targetId}&num_hashtags=${hashtag}&tone=${tone}&social_media=${platformId}`,{
            headers:{
                Authorization: `Bearer ${token}`
            },
            withCredentials: true
        }).then(res=>{
            setLoading(false);
            setcaption(res.data.Caption);
            navigate("/caption",{state:{caption:res.data.Caption, file_path:res.data.File_PATH}})
        }).catch(err=>{
            setLoading(false);
            console.log(err);
        })


    }
    //To handle Logout
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
    // Handling mouse move
    const handleHashtag = (e)=>{
        setHashtag(e.target.value);
        const x = (hashtag / 30) * 100;
        const gradient = (x!=0)?`linear-gradient(90deg, #1C4042 ${x}%, #E9A9CC${x}%`: "#E9A9CC";
        e.target.style.backgroundImage = gradient;
    }

  return (
    <>
    <div>
        <div className="header-page2">
            <div>
                <p>ExplAIstic</p>
            </div>
            <div className= "icons-page2">
            <i
                className={`fa-regular fa-user ${showDropdown ? 'active' : ''}`}
                onClick={toggleDropdown}
              ></i>
            <i className="fa-solid fa-bars"></i>
            </div>
        </div>
        <section>
        <div className="content-page2">
            {showDropdown && (
                <div className="dropdown-input">
                <ul>
                    <li onClick={handleLogout}>Log out</li>
                </ul>
                </div>
            )}
            <div className="innerContent-page2">
                <p className="steps" style ={{marginBottom:"40px"}}>Choose Preference</p>
                <div className="caption-size">
                <div >
                    <p className="label">Caption Size ?</p>
                </div>
                <div className='captionSize-icons'>
                    <div>
                    <i className="fa-solid fa-align-center captionSize small-i" id = "small" style = {selectSizeId === "small" ? selectdiv:styles} onClick = {(e)=>handleSize(e.target.id)}></i>
                    <p style= {{fontSize:"14px",textAlign:"center"}}>small</p>

                    </div>
                    <div>
                    <i className="fa-solid fa-align-center captionSize medium" id = "medium" style = {selectSizeId === "medium" ? selectdiv:styles} onClick = {(e)=>handleSize(e.target.id)}></i>
                    <p style= {{fontSize:"14px",textAlign:"center"}}>medium</p>

                    </div>
                    <div>
                    <i className="fa-solid fa-align-center captionSize large" id = "large" style = {selectSizeId === "large" ? selectdiv:styles} onClick = {(e)=>handleSize(e.target.id)}></i>
                    <p style= {{fontSize:"14px",textAlign:"center"}}>large</p>


                    </div>
                    <div>
                    <i className="fa-solid fa-align-center captionSize extra-large" id = "very-large" style = {selectSizeId === "very large" ? selectdiv:styles} onClick = {()=>handleSize("very large")}></i>
                    <p style= {{fontSize:"14px",textAlign:"center"}}>extra large</p>

                    </div>
                    <div>
                    <i className="fa-solid fa-align-center captionSize blog-post" id = "blog-post" style = {selectSizeId === "blog post" ? selectdiv:styles} onClick = {()=>handleSize("blog post")}></i>
                    <p style= {{fontSize:"14px",textAlign:"center"}}>Blog Post</p>


                    </div>
                    </div>



                </div>
                <div className="style-hashtag-heading">
                    <div className='preference_heading'>
                    <p className="label " style={{marginTop:"20px",}}>Caption Style ?</p>
                    </div>
                    <div className='preference_heading'>
                    <p className="label " style={{marginTop:"20px",}}>Hashtags ?</p>
                    </div>
                </div>
                <div className="style-hashtag">
                    <div className="caption-style">
                    
                <div className='captionStyle-icons'>
                    <div className='captionStyle'  id = "cool" onClick={(e)=>handleChange(e.target.id)}  style = {targetId === "cool" ? selectdiv:styles}>
                        Cool
                    </div>
                    <div className='captionStyle'  id ="professional" onClick={(e)=>handleChange(e.target.id)} style = {targetId === "professional" ? selectdiv:styles}>
                        Professional
                    </div>
                    <div className='captionStyle'  id = "artistic" onClick={(e)=>handleChange(e.target.id)} style = {targetId === "artistic" ? selectdiv:styles}>
                        Artistic
                    </div>
                    <div className='captionStyle'  id = "poetic" onClick={(e)=>handleChange(e.target.id)} style = {targetId === "poetic" ? selectdiv:styles}>
                        Poetic
                    </div>
                    <div className='captionStyle'  id = "poetry" onClick={(e)=>handleChange(e.target.id)} style = {targetId === "poetry" ? selectdiv:styles}>
                        Poetry
                    </div>
                </div>
                    </div>
                    <div className="hashtags">
                            <input type="range" value={hashtag} min="0" max="30"  onChange = {handleHashtag} />
                            <p className='hash'>{hashtag}</p>
                    </div>
                </div>
                
                <div className='preferences'>
                    <div className='captionTone'>
                        <p className="label tone" style={{marginTop:"0px",marginBottom:"0px"}}>Caption Tone ?</p>
                        <div className='dropdown-wrapper'>
                            <select className='dropdown' onChange = {(e)=>setTone(e.target.value)} onClick={(e) => { console.log(e.target.value) }}>
                                <option selected>Casual</option>
                                <option>Humorous</option>
                                <option>Inspirational</option>
                                <option>Conversational</option>
                                <option>Educational</option>
                                <option>Storytelling</option>
                                <option>Sentimental</option>
                            </select>
                        </div>
                    </div>
                    <div className='preffered-platform'>
                        <p className="label" style={{marginTop:"0px",marginBottom:"15px"}}>Preferred PlatForm?</p>
                        <div className='socialHandle-icons'>
                        <div id = "facebook" style = {{width:"50px",height:"50px",display:"flex"}}>
                        <img  onClick={(e)=>handleFacebook("facebook")} style = {platformId == "facebook" ?addBorder:bordernone}  src={facebook} alt="facebook"></img>
                        </div>
                        <div id = "instagram" style = {{width:"50px",height:"50px",position:"relative",display:"flex"}}>
                        <img  onClick={(e)=>handleInstagram("instagram")} style = {platformId == "instagram" ?addBorder:bordernone}  src={instagram} alt="instagram"></img>

                        </div>
                        <div id = "twitter" style = {{width:"50px",height:"50px",display:"flex"}}>
                        <img  onClick={(e)=>handleTwitter("twitter")} style = {platformId == "twitter" ?addBorder:bordernone}  src={twitter} alt="twitter"></img>
                        </div>
                        <div id = "linkedin" style = {{width:"50px",height:"50px",display:"flex"}}>
                        <img  onClick={(e)=>handleLinkedIn("linkedin")} style = {platformId == "linkedin" ?addBorder:bordernone}  src={linkedin} alt="linkedin"></img>
                        </div>

                    </div>
                    </div>
                </div>
                {
                    loading?<div className="spinners">
                        <Circles
                        height="50"
                        width="50"
                        color="#1c4042"
                        ariaLabel="circles-loading"
                        wrapperStyle={{}}
                        wrapperClass=""
                        visible={true}
                        ></Circles>
                    </div>:<button className="btn-style-page2" style = {{border:"none"}} onClick ={generateCaption}>Generate Caption</button>
                  }
           </div>           
        </div>
        <div className="footer-page2">
        </div>
        </section>
         <div className="images-page2">
        </div>
        
    </div>
   
    </>
    
  )
}

export default ChooseCaption