import React from "react"
import "./footer.css"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLinkedin, faXTwitter, faInstagram } from '@fortawesome/free-brands-svg-icons';

const Footer = () => {
  return (
    <>
      <footer>
        <div className='container padding'>
          <div className='logo'>
            <h1><a href='/'>MentalGlow-AI</a></h1>
            <span>AI-Powered Mental Wellness Platform</span>
            <p>Platform that helps individuals monitor their emotional well-being, get relaxation recommendations, and connect with others for support. </p>
            <div className='social-icons'>
              <i className='footicon'><a href="/"><FontAwesomeIcon icon={faLinkedin} /></a></i>
              <i className='footicon'><a href="/"><FontAwesomeIcon icon={faXTwitter} /></a></i>
              <i className='footicon'><a href="/"><FontAwesomeIcon icon={faInstagram} /></a></i>
            </div>
          </div>
          <div className='box link'>
            <h3>Explore</h3>
            <ul>
              <li><a href="/about" className="footlink">About Us</a></li>
              <li><a href="/journal" className="footlink">Blog</a></li>
              <li><a href="/checkup" className="footlink">Checkup</a></li>
            </ul>
          </div>
          <div className='box link'>
            <h3>Quick Links</h3>
            <ul>
              <li><a href="/contact" className="footlink">Contact Us</a></li>
              <li><a href="/T&C" className="footlink">Terms & Conditions</a></li>
              <li><a href="/privacy" className="footlink">Privacy</a></li>
            </ul>
          </div>
          <div className='box last'>
            <h3>Have a Questions?</h3>
            <ul>
              <li>
                <i className='fa fa-map'></i>
                Faridabad, 121001, Haryana, India
              </li>
              <li>
                <i className='fa fa-phone-alt'></i>
                +91 70******31
              </li>
              <li>
                <i className='fa fa-paper-plane'></i>
                mentalglow-ai@gmail.com
              </li>
            </ul>
          </div>
        </div>
      </footer>
      <div className='legal'>
        <p>
          <a href="/">© 2025 MentalGlow-ai. All rights reserved.</a>
        </p>
      </div>
    </>
  )
}

export default Footer
