import React from "react";
import { useDispatch } from "react-redux";
import authService from "../../appwrite/auth";
import { logout } from "../../store/authSlice";

function LogoutBtn() {
  const dispatch = useDispatch();
  const logoutHandler = () => {
    authService.logout().then(() => {
      dispatch(logout());
    });
  };

  return (
    <button
      className="inline-block px-6 py-2 duration-200 rounded-full"
      style={{
        backgroundColor: "black", // Slightly darker gray background
        color: "#FFFFF", // Dark gray text for contrast

        fontWeight: "bold",
      }}
      onClick={logoutHandler}
      onMouseEnter={(e) => {
        e.target.style.backgroundColor = "#B0B3B8"; // Darker gray on hover
      }}
    >
      Logout
    </button>
  );
}

export default LogoutBtn;
