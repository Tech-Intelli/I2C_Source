import React,{useState} from 'react';
import Modal from 'react-bootstrap/Modal';
import "./SignModal.css"
import facebook from "../assets/icons/facebook.svg";
import instagram from "../assets/icons/instagram.svg";
import twitter from "../assets/icons/twitter.svg";
import linkedin from "../assets/icons/linkedin.svg";
import { Link, useNavigate } from 'react-router-dom';
import axios from "axios";
import {Circles} from "react-loader-spinner"

export function SignInModal(props) {
  const navigate = useNavigate();
  const [forgotPassword, setForgotPassword] = useState(false);
  const [login, setLogin] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(false);
  const [errorText, setErrorText] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!email || !password) {
      console.log('Please enter all fields');
    } else {
      setLoading(true);
      const body = {
        email: email,
        password: password
      };
      await axios
        .post(`${process.env.REACT_APP_BACKEND_URL}/login_user`, body)
        .then(res => {
          setLoading(false);
          localStorage.setItem('token', res.data.token);
          navigate('/uploadfile');
        })
        .catch(err => {
          console.log(err);
          setLoading(false);
          setError(true);
          setErrorText("*Invalid credentials. Please enter email and password correctly")
        });
    }
  };

  const handleGuestLogin = async () => {
    await axios
      .post(`${process.env.REACT_APP_BACKEND_URL}/login_as_guest`)
      .then(res => {
        setLoading(false);
        localStorage.setItem('token', res.data.token);
        navigate('/uploadfile');
      })
      .catch(err => {
        console.log(err);
      });
  };

  const handleSignUp = async () => {
    if (!email || !password) {
      setError(true);
      setErrorText('Please enter all fields');
    } else {
      setError(false);
      if (password !== confirmPassword) {
        setError(true);
        setErrorText("Passwords don't match!");
      } else {
        setLoading(true);
        setError(false);
        const body = {
          email: email,
          password: password
        };
        await axios
          .post(`${process.env.REACT_APP_BACKEND_URL}/register_user`, body)
          .then(res => {
            setSuccess('User registered successfully! Please verify your email to login!');
            setLoading(false);
            setEmail('');
            setPassword('');
            setConfirmPassword('');
          })
          .catch(err => {
            console.log(err);
          });
      }
    }
  };

  const handleResetPassword = async () => {
    if (!email || !password || !confirmPassword) {
      setError(true);
      setErrorText('Please enter all fields');
    } else if (password !== confirmPassword) {
      setError(true);
      setErrorText("Passwords don't match!");
    } else {
      setLoading(true);
      setError(false);
      const body = {
        username: email,
        password: confirmPassword
      };
      await axios
        .post(`${process.env.REACT_APP_BACKEND_URL}/forget_password`, body)
        .then(res => {
          setLoading(false);
          setSuccess('Password has been changed successfully. You can now login with the new password.');
          setEmail('');
          setPassword('');
          setConfirmPassword('');
        })
        .catch(err => {
          console.log(err);
        });
    }
  };

  return (
    <>
      <Modal className="SignModal" show={props.show} onHide={props.handleClose} keyboard={false}>
        {!login ? (
          <div>
            <Modal.Title>
              Sign Up {error ? <p className="errorText">{errorText}</p> : null}
            </Modal.Title>

            <input
              placeholder="Enter email"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
            <input
              placeholder="Enter Password"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
            <input
              placeholder="Confirm Password"
              type="password"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
            />
            {!success ? (
              loading ? (
                <>
                  <div className="spinners">
                    <Circles
                      height="50"
                      width="50"
                      color="#E9FDFF"
                      ariaLabel="circles-loading"
                      wrapperStyle={{}}
                      wrapperClass=""
                      visible={true}
                    />
                  </div>
                </>
              ) : (
                <button className="btn-style modal-btn-btn" onClick={handleSignUp}>
                  Sign Up
                </button>
              )
            ) : (
              <p className="success">{success}</p>
            )}
            <hr className="hr-text" data-content="OR" />
            {/* <div className="socialHandles">
              <img src={facebook} alt="facebook" />
              <img src={instagram} alt="instagram" />
              <img src={twitter} alt="twitter" />
              <img src={linkedin} alt="linkedin" />
            </div> */}
            <div className="modalFooter">
              <p>
                Already a user? <span onClick={() => setLogin(!login)}>LOGIN</span>
              </p>
              <span onClick={handleGuestLogin}>LOGIN as Guest</span>
            </div>
          </div>
        ) : (
          <div className="Login">
            {!forgotPassword ? (
              <>
                <Modal.Title>Sign In</Modal.Title>
                <input
                  placeholder="Enter email or mobile"
                  onChange={e => setEmail(e.target.value)}
                />
                <input
                  placeholder="Enter Password"
                  type="password"
                  onChange={e => {
                    setPassword(e.target.value);
                  }}
                />
                <div className="forgot-password">
                  <span onClick={() => setForgotPassword(true)}>Forgot Password?</span>
                </div>
                {error ? <p className="errorText">{errorText}</p> : null}
                {loading ? (
                  <>
                    <div className="spinners">
                      <Circles
                        height="50"
                        width="50"
                        color="#E9FDFF"
                        ariaLabel="circles-loading"
                        wrapperStyle={{}}
                        wrapperClass=""
                        visible={true}
                      />
                    </div>
                  </>
                ) : (
                  <button className="btn-style modal-btn-btn" onClick={handleLogin}>
                    Login
                  </button>
                )}
              </>
            ) : (
              <>
                <Modal.Title>Reset Password</Modal.Title>
                <input
                  placeholder="Enter username or email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                />
                <input
                  placeholder="Enter new password"
                  type="password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                />
                <input
                  placeholder="Confirm new password"
                  type="password"
                  value={confirmPassword}
                  onChange={e => setConfirmPassword(e.target.value)}
                />
                {error ? <p className="errorText">{errorText}</p> : null}
                {!success ? (
                  loading ? (
                    <>
                      <div className="spinners">
                        <Circles
                          height="50"
                          width="50"
                          color="#E9FDFF"
                          ariaLabel="circles-loading"
                          wrapperStyle={{}}
                          wrapperClass=""
                          visible={true}
                        />
                      </div>
                    </>
                  ) : (
                    <button className="btn-style modal-btn-btn" onClick={handleResetPassword}>
                      Reset Password
                    </button>
                  )
                ) : (
                  <p className="success">{success}</p>
                )}
              </>
            )}
            <hr className="hr-text" data-content="OR" />
            {/* <div className="socialHandles">
              <img src={facebook} alt="facebook" />
              <img src={instagram} alt="instagram" />
              <img src={twitter} alt="twitter" />
              <img src={linkedin} alt="linkedin" />
            </div> */}
            <div className="modalFooter">
              <p>
                Not a user? <span onClick={() => setLogin(!login)}>SIGN UP</span>
              </p>
              <span onClick={handleGuestLogin}>LOGIN as Guest</span>
            </div>
          </div>
        )}
      </Modal>
    </>
  );
}