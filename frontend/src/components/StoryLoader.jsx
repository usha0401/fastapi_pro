// import {useState, useEffect} from 'react';
// import {useParams, useNavigate} from "react-router-dom"
// import axios from 'axios';
// import LoadingStatus from "./LoadingStatus.jsx";
// import StoryGame from "./StoryGame.jsx";
// import {API_BASE_URL} from "../util.js";


// function StoryLoader() {
//     const {id} = useParams();
//     const navigate = useNavigate();
//     const [story, setStory] = useState(null);
//     const [loading, setLoading] = useState(true)
//     const [error, setError] = useState(null);
    

//     useEffect(() => {
//         loadStory(id)
//     }, [id])

//     const loadStory = async (storyId) => {
//         setLoading(true)
//         setError(null)

//         try {
//             const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`)
//             setStory(response.data)
//             setLoading(false)
//         } catch (err) {
//             if (err.response?.status === 404) {
//                 setError("Story is not found.")
//             } else {
//                 setError("Failed to load story")
//             }
//         } finally {
//             setLoading(false)
//         }
//     }

//     const createNewStory = () => {
//         navigate("/")
//     }

//     if (loading) {
//         return <LoadingStatus theme={"story"} />
//     }

//     if (error) {
//         return <div className="story-loader">
//             <div className="error-message">
//                 <h2>Story Not Found</h2>
//                 <p>{error}</p>
//                 <button onClick={createNewStory}>Go to Story Generator</button>
//             </div>
//         </div>
//     }

//     if (story) {
//         return <div className="story-loader">
//             <StoryGame story={story} onNewStory={createNewStory} />
//         </div>
//     }
// }

// export default StoryLoader;

import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import LoadingStatus from "./LoadingStatus.jsx";
import StoryGame from "./StoryGame.jsx";
import { API_BASE_URL } from "../util.js";

function StoryLoader() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [suggestions, setSuggestions] = useState([]);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);

  // Load story
  useEffect(() => {
    loadStory(id);
  }, [id]);

  const loadStory = async (storyId) => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(
        `${API_BASE_URL}/stories/${storyId}/complete`
      );
      setStory(response.data);
    } catch (err) {
      if (err.response?.status === 404) {
        setError("Story not found.");
      } else {
        setError("Failed to load story.");
      }
    } finally {
      setLoading(false);
    }
  };

  // Mock AI suggestions (OpenAI-ready)
  useEffect(() => {
    if (!story?.root_node?.content || suggestions.length > 0) return;

    setLoadingSuggestions(true);

    setTimeout(() => {
      setSuggestions([
        "Explore the surroundings",
        "Talk to someone nearby",
        "Move forward cautiously"
      ]);
      setLoadingSuggestions(false);
    }, 600);
  }, [story]);

  const createNewStory = () => {
    navigate("/");
  };

  if (loading) {
    return <LoadingStatus theme="story" />;
  }

  if (error) {
    return (
      <div className="story-loader">
        <div className="error-message">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={createNewStory}>Create New Story</button>
        </div>
      </div>
    );
  }

  return (
    <div className="story-loader">
      <StoryGame
        story={story}
        suggestions={suggestions}
        loadingSuggestions={loadingSuggestions}
        onNewStory={createNewStory}
      />
    </div>
  );
}

export default StoryLoader;
