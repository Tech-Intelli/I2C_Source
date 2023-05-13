import React, { useState } from 'react'
import "./ChooseCaption.css"
import facebook from "./facebook.svg";
import instagram from "./instagram.svg";
import twitter from "./twitter.svg";
import linkedin from "./linkedin.svg";
import { Link } from 'react-router-dom';

const ChooseCaption = () => {
    
    const [targetId, settargetId] = useState();
    const [selectSizeId,setSelectsizeId] = useState();
    const [platformId, setplatformId] = useState();
    const fillColor = {
        fill:"blue",
    }

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
        console.log(id);
        setplatformId(id);
    }

    const handleTwitter= (id)=>{
        console.log(id);
        setplatformId(id);
    }
    const handleInstagram = (id)=>{
        console.log(id);
        setplatformId(id);
    }
    const handleLinkedIn = (id)=>{
        console.log(id);
        setplatformId(id);
    }
  return (
    <>
    <div className='page-2'>
        <div className="header-page2">
            <div>
                <p>ExplAIstic</p>
            </div>
            <div className= "icons-page2">
                <i className="fa-regular fa-user"></i>
                <i className="fa-solid fa-bars"></i>
            </div>
        </div>
        <section>
        <div className="content-page2">
            <div className="innerContent-page2">
                <p className="steps" style ={{marginBottom:"40px"}}>Step 2 :Choose Preference</p>
                <div >
                    <p className="label">Caption Size ?</p>
                </div>
                <div className='captionSize-icons'>
                    <div>
                    <i class="fa-solid fa-align-center captionSize small-i" id = "small" style = {selectSizeId === "small" ? selectdiv:styles} onClick = {(e)=>handleSize(e.target.id)}></i>
                    <p style= {{fontSize:"14px",textAlign:"center"}}>small</p>

                    </div>
                    <div>
                    <i class="fa-solid fa-align-center captionSize medium" id = "medium" style = {selectSizeId === "medium" ? selectdiv:styles} onClick = {(e)=>handleSize(e.target.id)}></i>
                    <p style= {{fontSize:"14px",textAlign:"center"}}>medium</p>

                    </div>
                    <div>
                    <i class="fa-solid fa-align-center captionSize large" id = "large" style = {selectSizeId === "large" ? selectdiv:styles} onClick = {(e)=>handleSize(e.target.id)}></i>
                    <p style= {{fontSize:"14px",textAlign:"center"}}>large</p>


                    </div>
                    <div>
                    <i class="fa-solid fa-align-center captionSize extra-large" id = "extra-large" style = {selectSizeId === "extra-large" ? selectdiv:styles} onClick = {(e)=>handleSize(e.target.id)}></i>
                    <p style= {{fontSize:"14px",textAlign:"center"}}>extra large</p>

                    </div>
                    <div>
                    <i class="fa-solid fa-align-center captionSize blog-post" id = "blog-post" style = {selectSizeId === "blog-post" ? selectdiv:styles} onClick = {(e)=>handleSize(e.target.id)}></i>
                    <p style= {{fontSize:"14px",textAlign:"center"}}>Blog Post</p>


                    </div>




                </div>
                <div className='preference_heading'>
                <p className="label" style={{marginTop:"20px",}}>Caption Style ?</p>
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
                <div className='preferences'>
                    <div className='captionTone'>
                        <p className="label" style={{marginTop:"0px",marginBottom:"0px"}}>Caption Tone ?</p>
                        <div className='dropdown-wrapper'>
                            <select className='dropdown'>
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
                        <p className="label" style={{marginTop:"0px",marginBottom:"15px"}}>Preffered PlatForm?</p>
                        <div className='socialHandle-icons'>
                        {/* <img src ={facebook} alt= "facebook" style = {{border:"1px solid #1C4042",padding:"none"}}></img> */}

                        {/* <svg style = {{border:"4px solid #1C4042"}} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M400 32H48A48 48 0 0 0 0 80v352a48 48 0 0 0 48 48h137.25V327.69h-63V256h63v-54.64c0-62.15 37-96.48 93.67-96.48 27.14 0 55.52 4.84 55.52 4.84v61h-31.27c-30.81 0-40.42 19.12-40.42 38.73V256h68.78l-11 71.69h-57.78V480H400a48 48 0 0 0 48-48V80a48 48 0 0 0-48-48z"/></svg> */}
                        <div id = "facebook" style = {{width:"50px",height:"50px",display:"flex"}}>
                        <svg width="50" height="50" viewBox="0 0 120 120" style = {platformId == "facebook" ?addBorder:bordernone} id= "facebook" onClick={(e)=>handleFacebook("facebook")} fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M112.65 0.830002H7.35996C3.75354 0.830002 0.829956 3.75358 0.829956 7.36V112.65C0.829956 116.256 3.75354 119.18 7.35996 119.18H112.65C116.256 119.18 119.18 116.256 119.18 112.65V7.36C119.18 3.75358 116.256 0.830002 112.65 0.830002Z" fill="#3D5A98"/>
                        </svg>
                        </div>
                        <div id = "instagram" style = {{width:"50px",height:"50px",position:"relative",display:"flex"}}>
                        <svg width="50" height="50" viewBox="0 0 256 256" style = {platformId == "instagram" ?addBorder:bordernone } id= "instagram" onClick={(e)=>handleInstagram("instagram")} fill="none" xmlns="http://www.w3.org/2000/svg">
                            <g clip-path="url(#clip0_2_4)">
                            <path d="M196 0H60C26.8629 0 0 26.8629 0 60V196C0 229.137 26.8629 256 60 256H196C229.137 256 256 229.137 256 196V60C256 26.8629 229.137 0 196 0Z" fill="url(#paint0_radial_2_4)"/>
                            <path d="M196 0H60C26.8629 0 0 26.8629 0 60V196C0 229.137 26.8629 256 60 256H196C229.137 256 256 229.137 256 196V60C256 26.8629 229.137 0 196 0Z" fill="url(#paint1_radial_2_4)"/>
                            <path d="M128.009 28C100.851 28 97.442 28.119 86.776 28.604C76.13 29.092 68.863 30.777 62.505 33.25C55.927 35.804 50.348 39.221 44.79 44.781C39.227 50.34 35.81 55.919 33.248 62.494C30.768 68.854 29.081 76.124 28.602 86.765C28.125 97.432 28 100.842 28 128.001C28 155.16 28.12 158.558 28.604 169.224C29.094 179.87 30.779 187.137 33.25 193.495C35.806 200.073 39.223 205.652 44.783 211.21C50.34 216.773 55.919 220.198 62.492 222.752C68.855 225.225 76.123 226.91 86.767 227.398C97.434 227.883 100.84 228.002 127.997 228.002C155.158 228.002 158.556 227.883 169.222 227.398C179.868 226.91 187.143 225.225 193.506 222.752C200.081 220.198 205.652 216.773 211.208 211.21C216.771 205.652 220.187 200.073 222.75 193.498C225.208 187.137 226.896 179.868 227.396 169.226C227.875 158.56 228 155.16 228 128.001C228 100.842 227.875 97.434 227.396 86.767C226.896 76.121 225.208 68.855 222.75 62.497C220.187 55.919 216.771 50.34 211.208 44.781C205.646 39.219 200.083 35.802 193.5 33.251C187.125 30.777 179.854 29.091 169.208 28.604C158.541 28.119 155.145 28 127.978 28H128.009ZM119.038 46.021C121.701 46.017 124.672 46.021 128.009 46.021C154.71 46.021 157.874 46.117 168.418 46.596C178.168 47.042 183.46 48.671 186.985 50.04C191.652 51.852 194.979 54.019 198.477 57.52C201.977 61.02 204.143 64.353 205.96 69.02C207.329 72.54 208.96 77.832 209.404 87.582C209.883 98.124 209.987 101.29 209.987 127.978C209.987 154.666 209.883 157.833 209.404 168.374C208.958 178.124 207.329 183.416 205.96 186.937C204.148 191.604 201.977 194.927 198.477 198.425C194.977 201.925 191.654 204.091 186.985 205.904C183.464 207.279 178.168 208.904 168.418 209.35C157.876 209.829 154.71 209.933 128.009 209.933C101.307 209.933 98.142 209.829 87.601 209.35C77.851 208.9 72.559 207.271 69.031 205.902C64.365 204.089 61.031 201.923 57.531 198.423C54.031 194.923 51.865 191.598 50.048 186.929C48.679 183.408 47.048 178.116 46.604 168.366C46.125 157.824 46.029 154.658 46.029 127.953C46.029 101.249 46.125 98.099 46.604 87.557C47.05 77.807 48.679 72.515 50.048 68.99C51.861 64.323 54.031 60.99 57.532 57.49C61.032 53.99 64.365 51.823 69.032 50.007C72.557 48.632 77.851 47.007 87.601 46.559C96.826 46.142 100.401 46.017 119.038 45.996V46.021ZM181.389 62.625C174.764 62.625 169.389 67.995 169.389 74.621C169.389 81.246 174.764 86.621 181.389 86.621C188.014 86.621 193.389 81.246 193.389 74.621C193.389 67.996 188.014 62.621 181.389 62.621V62.625ZM128.009 76.646C99.649 76.646 76.655 99.64 76.655 128.001C76.655 156.362 99.649 179.345 128.009 179.345C156.37 179.345 179.356 156.362 179.356 128.001C179.356 99.641 156.368 76.646 128.007 76.646H128.009ZM128.009 94.667C146.418 94.667 161.343 109.59 161.343 128.001C161.343 146.41 146.418 161.335 128.009 161.335C109.599 161.335 94.676 146.41 94.676 128.001C94.676 109.59 109.599 94.667 128.009 94.667Z" fill="white"/>
                            </g>
                            <defs>
                            <radialGradient id="paint0_radial_2_4" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(68 275.717) rotate(-90) scale(253.715 235.975)">
                            <stop stop-color="#FFDD55"/>
                            <stop offset="0.1" stop-color="#FFDD55"/>
                            <stop offset="0.5" stop-color="#FF543E"/>
                            <stop offset="1" stop-color="#C837AB"/>
                            </radialGradient>
                            <radialGradient id="paint1_radial_2_4" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(-42.881 18.441) rotate(78.681) scale(113.412 467.488)">
                            <stop stop-color="#3771C8"/>
                            <stop offset="0.128" stop-color="#3771C8"/>
                            <stop offset="1" stop-color="#6600FF" stop-opacity="0"/>
                            </radialGradient>
                            <clipPath id="clip0_2_4">
                            <rect width="256" height="256" fill="white"/>
                            </clipPath>
                            </defs>
                        </svg>
                        </div>
                        <div id = "twitter" style = {{width:"50px",height:"50px",display:"flex"}}>
                        <svg width="50" height="50" viewBox="0 0 256 209" style = {platformId == "twitter" ?addBorder:bordernone} id= "twitter" onClick={(e)=>handleTwitter("twitter")} fill="none" xmlns="http://www.w3.org/2000/svg">
                            <g clip-path="url(#clip0_10_7)">
                            <path d="M256 25.45C246.414 29.6968 236.246 32.4843 225.834 33.72C236.679 27.22 245.006 16.927 248.927 4.66301C238.618 10.7809 227.338 15.0913 215.576 17.408C205.995 7.20101 192.346 0.822006 177.239 0.822006C148.233 0.822006 124.716 24.338 124.716 53.342C124.716 57.459 125.181 61.467 126.076 65.312C82.426 63.121 43.726 42.212 17.821 10.436C13.301 18.193 10.711 27.216 10.711 36.84C10.711 55.062 19.984 71.137 34.076 80.556C25.7355 80.2948 17.5785 78.0421 10.286 73.986C10.283 74.206 10.283 74.426 10.283 74.647C10.283 100.094 28.387 121.322 52.413 126.147C44.6789 128.25 36.5663 128.558 28.695 127.047C35.378 147.913 54.775 163.097 77.757 163.522C59.782 177.608 37.135 186.005 12.529 186.005C8.289 186.005 4.109 185.756 0 185.271C23.243 200.173 50.85 208.868 80.51 208.868C177.117 208.868 229.944 128.837 229.944 59.433C229.944 57.155 229.894 54.89 229.792 52.638C240.074 45.2049 248.949 35.9982 256 25.45Z" fill="#55ACEE"/>
                            </g>
                            <defs>
                            <clipPath id="clip0_10_7">
                            <rect width="256" height="209" fill="white"/>
                            </clipPath>
                            </defs>
                        </svg>
                        </div>
                        <div id = "linkedin" style = {{width:"50px",height:"50px",display:"flex"}}>
                        <svg width="50" height="50" viewBox="0 0 256 256" style = {platformId == "linkedin" ?addBorder:bordernone} id= "linkedin" onClick={(e)=>handleLinkedIn("linkedin")} fill="none" xmlns="http://www.w3.org/2000/svg">
                            <g clip-path="url(#clip0_10_2)">
                            <path d="M218.123 218.127H180.192V158.724C180.192 144.559 179.939 126.324 160.464 126.324C140.708 126.324 137.685 141.758 137.685 157.693V218.123H99.755V95.967H136.168V112.661H136.678C140.322 106.43 145.588 101.304 151.915 97.8292C158.242 94.3542 165.393 92.6604 172.606 92.928C211.051 92.928 218.139 118.216 218.139 151.114L218.123 218.127ZM56.955 79.27C44.798 79.272 34.941 69.418 34.939 57.261C34.937 45.104 44.79 35.247 56.947 35.245C69.104 35.242 78.961 45.096 78.963 57.253C78.9641 63.091 76.646 68.6904 72.5187 72.8194C68.3915 76.9483 62.7931 79.2687 56.955 79.27ZM75.921 218.128H37.95V95.967H75.92V218.127L75.921 218.128ZM237.033 0.0180063H18.89C8.58002 -0.0979937 0.125023 8.16101 -0.000976562 18.471V237.524C0.121023 247.839 8.57502 256.106 18.889 255.998H237.033C247.369 256.126 255.856 247.859 255.999 237.524V18.454C255.852 8.12401 247.364 -0.133994 237.033 0.00100628" fill="#0A66C2"/>
                            </g>
                            <defs>
                            <clipPath id="clip0_10_2">
                            <rect width="256" height="256" fill="white"/>
                            </clipPath>
                            </defs>
                        </svg>
                        </div>

                    </div>
                    </div>
                </div>
                <Link to= "/caption"><button className="btn-style-page2" style = {{border:"none"}}>Generate Caption</button></Link>
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