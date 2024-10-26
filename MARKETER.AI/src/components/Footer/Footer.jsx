import React from "react";
import { Link } from "react-router-dom";
import Logo from "../Logo";

function Footer() {
  // Define colors to match your theme
  const footerBackground = "linear-gradient(to right, #C4D7FF, #FFD7C4)"; // Gradient for the footer
  const textColor = "#1C1C1E"; // Dark text for readability
  const linkColor = "#003366"; // Dark blue for links
  const hoverColor = "#87A2FF"; // Lighter blue for hover effect

  return (
    <section
      className="relative overflow-hidden py-10"
      style={{ background: footerBackground, borderTop: "2px solid #1A1A2E" }}
    >
      <div className="relative z-10 mx-auto max-w-7xl px-4">
        <div className="-m-6 flex flex-wrap">
          <div className="w-full p-6 md:w-1/2 lg:w-5/12">
            <div className="flex h-full flex-col justify-between">
              <div className="mb-4 inline-flex items-center">
                <Logo width="100px" />
              </div>
              <div>
                <p className="text-sm" style={{ color: textColor }}>
                  &copy; Copyright 2023. All Rights Reserved by DevUI.
                </p>
              </div>
            </div>
          </div>
          <div className="w-full p-6 md:w-1/2 lg:w-2/12">
            <div className="h-full">
              <h3 className="tracking-px mb-9 text-xs font-semibold uppercase text-gray-600">
                Company
              </h3>
              <ul>
                <li className="mb-4">
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Features
                  </Link>
                </li>
                <li className="mb-4">
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Pricing
                  </Link>
                </li>
                <li className="mb-4">
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Affiliate Program
                  </Link>
                </li>
                <li>
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Press Kit
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="w-full p-6 md:w-1/2 lg:w-2/12">
            <div className="h-full">
              <h3 className="tracking-px mb-9 text-xs font-semibold uppercase text-gray-600">
                Support
              </h3>
              <ul>
                <li className="mb-4">
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Account
                  </Link>
                </li>
                <li className="mb-4">
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Help
                  </Link>
                </li>
                <li className="mb-4">
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Contact Us
                  </Link>
                </li>
                <li>
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Customer Support
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="w-full p-6 md:w-1/2 lg:w-3/12">
            <div className="h-full">
              <h3 className="tracking-px mb-9 text-xs font-semibold uppercase text-gray-600">
                Legals
              </h3>
              <ul>
                <li className="mb-4">
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Terms &amp; Conditions
                  </Link>
                </li>
                <li className="mb-4">
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link
                    className="text-base font-medium"
                    to="/"
                    style={{ color: linkColor, transition: "color 0.3s" }}
                    onMouseOver={(e) =>
                      (e.currentTarget.style.color = hoverColor)
                    }
                    onMouseOut={(e) =>
                      (e.currentTarget.style.color = linkColor)
                    }
                  >
                    Licensing
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Footer;
