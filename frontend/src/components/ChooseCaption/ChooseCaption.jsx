import React, { useState } from 'react'
import "./ChooseCaption.css"
import { useNavigate, useLocation } from 'react-router-dom';
import axios from "axios"
import { Circles } from "react-loader-spinner";
import facebook from "../assets/icons/facebook.svg";
import instagram from "../assets/icons/instagram.svg";
import twitter from "../assets/icons/twitter.svg";
import linkedin from "../assets/icons/linkedin.svg";
import Navbar from "../Navbar/Navbar";
import {Slider} from '@mui/material';

const ChooseCaption = () => {
    const location = useLocation()
    const token = localStorage.getItem('token')
    const [targetId, settargetId] = useState('cool');
    const [selectSizeId,setSelectsizeId] = useState('small');
    const [platformId, setplatformId] = useState('instagram');
    const [tone,setTone]=useState("Casual");
    const [caption,setcaption] =useState("");
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [hashtag, setHashtag] = useState(0); // Number of hashtags
    const addBorder = {
        border:"2px solid var(--bg-button)",
        borderRadius:"5px"
    }
    const bordernone = {
        border:"none",
    }


    const selectdiv = {
        backgroundColor :"var(--bg-button)",

        color : "#fff"
    }
    const styles = {
        background :"#2D2D2D",
        color:"var(--font-col)",
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
        const address = location?.state?.address || '';
        const file = location?.state?.file || '';
        axios.get(`${process.env.REACT_APP_BACKEND_URL}/generate_image_video_caption?caption_size=${selectSizeId}&context=${context}&style=${targetId}&num_hashtags=${hashtag}&tone=${tone}&social_media=${platformId}&file_name=${JSON.stringify(file)}&address=${address}`,{
            headers:{
                Authorization: `Bearer ${token}`
            },
            withCredentials: true
        }).then(res=>{
            setLoading(false);
            setcaption(res.data.Caption);
            navigate("/caption",{state:{caption:res.data.Caption,
                file_path:res.data.File_URL,
                context: context,
                address: address,
                file_name: file}})
        }).catch(err=>{
            setLoading(false);
            console.log(err);
        })


    }
    // Handling mouse move
    const handleHashtag = (e)=>{
        setHashtag(e.target.value);
    }

  return (
    <>
    <div>
        <Navbar flag={true}/>
        <section>
        <div className="content">
            <div className="innerContent-page2">

                <p className="steps" style ={{marginBottom:"40px"}}>Choose Preference</p>
                <div className="caption-size">
                <div >
                    <p className="label">Caption Size ?</p>
                </div>
                <div className='captionSize-icons'>
                    <p style= {selectSizeId === "small" ? selectdiv:styles} className='captionSize captionSize-text' id="small" onClick = {(e)=>handleSize(e.target.id)}>small</p>
                    <p style= {selectSizeId === "medium" ? selectdiv:styles} className='captionSize captionSize-text' id="medium" onClick = {(e)=>handleSize(e.target.id)}>medium</p>
                    <p style= {selectSizeId === "large" ? selectdiv:styles} className='captionSize captionSize-text' id="large" onClick = {(e)=>handleSize(e.target.id)}>large</p>
                    </div>



                </div>
                <div className="style-hashtag">
                    <div className="caption-style">
                        <div className='preference_heading'>
                            <p className="label " style={{marginTop:"20px",}}>Caption Style ?</p>
                        </div>
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
                        <div className='preference_heading'>
                        <p className="label " style={{marginTop:"20px",}}>Hashtags ?</p>
                        </div>
                            <Slider 
                                value={hashtag}
                                valueLabelDisplay='on'
                                onChange = {handleHashtag}
                                max={30}
                                min={0}
                                sx={{
                                    width: 200,
                                    color: 'var(--font-accent)',
                                    '& .MuiSlider-thumb': {
                                      backgroundColor: 'var(--bg-button)',
                                    },
                                    '& .MuiSlider-track': {
                                        backgroundColor: 'var(--bg-button-hov)',
                                        border: 'none',
                                      },
                                    '& .MuiSlider-valueLabel':{
                                        backgroundColor: 'var(--bg-button-hov)',
                                        color: 'var(--font-col)',
                                        height: 1,
                                        width: 1,
                                        fontSize: 14,
                                        fontFamily: 'Source Sans 3'
                                    }
                                      
                                  }}

                            />
                    </div>
                </div>
                
                <div className='preferences'>
                    <div className='captionTone'>
                        <p className="label tone" style={{marginTop:"0px",marginBottom:"0px"}}>Caption Tone ?</p>
                        <div className='dropdown-wrapper'>
                            <select className='dropdown' onChange = {(e)=>setTone(e.target.value)}>
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
                        color="var(--font-col)"
                        ariaLabel="circles-loading"
                        wrapperStyle={{}}
                        wrapperClass=""
                        visible={true}
                        ></Circles>
                        <p className="load-message">Generating the Caption. Grab a cup of tea or coffee in the meantime!!</p>
                    </div>:<button id = "generate_button"className="btn-style-page1" style = {{border:"none"}} onClick ={generateCaption}>Generate Caption</button>
                  }
           </div>           
        </div>
        <div className="footer-page2">
        </div>
        </section>
        
    </div>
   
    </>
    
  )
}

export default ChooseCaption