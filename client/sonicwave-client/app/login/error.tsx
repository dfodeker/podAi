"use client";
import React from "react";


const ErrorComponent = ({errorMsg}) => {
    return (
        <div className = "border-red-500 border-2 bg-red-100 m-2 p-4 rounded">
            <p>Error: {errorMsg}</p>
        </div>
    )
}

export default ErrorComponent;