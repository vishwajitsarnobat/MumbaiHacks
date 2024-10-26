import React from "react";
import appwriteService from "../appwrite/config";
import { Link } from "react-router-dom";

function PostCard({ $id, title, featuredImage }) {
  const imageUrl = appwriteService.getFilePreview(featuredImage); // Get the preview URL

  return (
    <Link to={`/post/${$id}`}>
      <div className="w-full bg-white rounded-xl border border-black shadow-lg p-4 transition-transform transform hover:scale-105">
        <div className="w-full flex justify-center mb-4">
          {imageUrl ? (
            <img
              src={imageUrl}
              alt={title}
              className="rounded-xl w-full h-auto"
            />
          ) : (
            <div className="w-full h-48 flex items-center justify-center bg-gray-200 rounded-xl">
              <span className="text-black text-lg">Image Not Available</span>
            </div>
          )}
        </div>
        <h2 className="text-xl font-bold text-black">{title}</h2>
      </div>
    </Link>
  );
}

export default PostCard;
