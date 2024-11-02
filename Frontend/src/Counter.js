import React from "react";
import { useSpring, animated } from "@react-spring/web";
import "./SectionDetails.css"; // Assuming you have CSS for styling

const SubmissionCounterCard = ({ title, totalSubmitted,speed }) => {

  // Use spring animation to animate count from 0 to totalSubmitted
  const { number } = useSpring({
    from: { number: 0 },
    to: { number: totalSubmitted },
    config: { duration: speed }, // Adjust duration as needed
  });

  return (
    <div className="section-card-counter">
      <h3>{title}</h3>
      <animated.div className="count-display">
        {number.to((n) => Math.floor(n))}
      </animated.div>
    </div>
  );
};

export default SubmissionCounterCard;
