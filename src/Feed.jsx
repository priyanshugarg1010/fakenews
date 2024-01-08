import { useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";

const Feed = () => {
  const [searchedText, setSearchedText] = useState("");
  const [searchEx, setSearchEx] = useState(false);
  const [isFakeNews, setIsFakeNews] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSearchEx(true);

    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", {
        news: searchedText,
      });

      // Assuming the backend response has a "LR Prediction" field
      const prediction = response.data["LR Prediction"];
      console.log(response.data["LR Prediction"]);

      // Update the state based on the prediction
      setIsFakeNews(prediction === "Fake News");
    } catch (error) {
      console.error("Error:", error);
      // Handle error as needed
    }
  };

  return (
    <>
      <section className="feed">
        <form className="relative w-full flex-center " onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Test news here..."
            value={searchedText}
            onChange={(e) => {
              setSearchedText(e.target.value);
              setSearchEx(false);
            }}
            required
            className={`search_input   peer ${
              searchEx ? "search_executed" : ""
            }`}
          />
        </form>

        {searchEx && isFakeNews !== "" && (
          <>
            {isFakeNews ? toast.error("Fake News") : toast.success("True News")}
          </>
        )}
      </section>
    </>
  );
};

export default Feed;
