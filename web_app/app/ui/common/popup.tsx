import { XMarkIcon, ExclamationCircleIcon } from "@heroicons/react/24/solid";
import { useEffect } from "react";

export function DeletePopup({
  showPopup,
  title,
  action,
}: {
  showPopup: (value: boolean) => void;
  title: string;
  action: () => void;
}) {
  useEffect(() => {
    const closePopup = (e: MouseEvent) => {
      const target = e.target as Element;
      if (target.id === "popup-overlay") {
        showPopup(false);
      }
    };
    window.addEventListener("click", closePopup);
    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        showPopup(false);
      }
    });
    return () => window.removeEventListener("click", closePopup);
  }, [showPopup]);

  const handleDeleteClick = () => {
    action();
    showPopup(false);
  };
  const handleCancelClick = () => showPopup(false);

  return (
    <div
      id="popup-overlay"
      className="fixed inset-0 z-10 flex justify-center items-center bg-black bg-opacity-50"
    >
      <div className="h-48 w-80 bg-white rounded-md flex flex-col justify-center items-center">
        <div className="flex items-center">
          <ExclamationCircleIcon className="w-12 text-pink-600" />
          <h2 className="text-gray-600 text-lg">
            確定刪除 <span className="font-semibold ">{title}</span> ?
          </h2>
        </div>
        <div className="flex justify-center items-center space-x-4 mt-4">
          <button
            className="px-3 py-2 border border-pink-600 text-pink-600 rounded-md hover:bg-pink-700 hover:text-white"
            onClick={handleDeleteClick}
          >
            確定刪除
          </button>
          <button
            className="px-3 py-2 border border-gray-600 text-gray-600 rounded-md hover:bg-gray-300"
            onClick={handleCancelClick}
          >
            取消
          </button>
        </div>
      </div>
      <button className="absolute top-4 right-4" onClick={handleCancelClick}>
        <XMarkIcon className="w-5 text-gray-600 hover:text-gray-400" />
      </button>
    </div>
  );
}
