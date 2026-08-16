import React from "react";

export default function WorkflowAnimation() {
  return (
    <div className="workflow-video-wrapper">
      <video
        className="workflow-video"
        autoPlay
        loop
        muted
        playsInline
        preload="auto"
      >
        <source
          src="/assets/cognify-workflow.mp4"
          type="video/mp4"
        />

        Your browser does not support the video tag.
      </video>
    </div>
  );
}