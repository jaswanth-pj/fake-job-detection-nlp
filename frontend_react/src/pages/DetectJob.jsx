  import JobImageForm from "../components/JobImageForm";
  import JobTextForm from "../components/JobTextForm";
  import "../styles/detectjob.css";
  import { useNavigate } from "react-router-dom";
  import { useEffect } from "react";
  import Navbaar from "../components/Navbaar";



  function DetectJob() {
    const navigate = useNavigate();

    // 🔐 Protect page (no login → redirect)
    useEffect(() => {
      const loggedIn = localStorage.getItem("isLoggedIn");
      if (!loggedIn) {
        navigate("/login");
      }
    }, []);

  
  

    return (
      <div className="detect-page">
        <Navbaar /> 

      

        {/* Hero */}
        <div className="detect-hero">
          <h1>Fake Job Detection</h1>
          <p>
            Analyze job descriptions and images using intelligent
            machine learning models to identify fraudulent postings.
          </p>
        </div>

        {/* Detection Panels */}
        <div className="detect-panels">
          <div className="detect-card">
            <h2>Text-Based Detection</h2>
            <JobTextForm />
          </div>

          <div className="detect-card">
            <h2>Image-Based Detection</h2>
            <JobImageForm />
          </div>
        </div>
      </div>
    );
  }

  export default DetectJob;
