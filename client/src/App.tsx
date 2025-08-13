import { Route, Routes } from "react-router-dom";
import "./App.css";
import Layout from "./Layout/Layout";
import Home from "./pages/Home/Home";
import Login from "./pages/Auth/Login";
import Signup from "./pages/Auth/Signup";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useMutation } from "@tanstack/react-query";
import { useDispatch } from "react-redux";
import { verify } from "./http/authApi";
import { verifyUser } from "./store/userAuth";
import { useEffect } from "react";
import CodeEditor from "./pages/CodeEditor/CodeEditor";
import { LabDetailPage } from "./pages/LabDetailsPage/LabDetailsPage";
import { LabListPage } from "./pages/LabListPage/LabListPage";
import TeacherDashboard from "./pages/StudentPerformance/StudentPerformance";
import ManageUsers from "./pages/AdminPage/AdminPage";

function App() {
  const dispatch = useDispatch();

  const mutation = useMutation({
    mutationFn: verify,
    onSuccess: (res) => {
      console.log(res.data);
      dispatch(verifyUser(res.data));
    },
  });

  useEffect(() => {
    mutation.mutate();
    // eslint-disable-next-line
  }, []);

  return (
    <>
      <Routes>
        <Route path="editor/:id" element={<CodeEditor />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="labs" element={<LabListPage />} />
          <Route path="labs/:id" element={<LabDetailPage />} />
          <Route path="performance/:id" element={<TeacherDashboard />} />
          <Route path="admin" element={<ManageUsers />} />
          <Route path="login" element={<Login />} />
          <Route path="signup" element={<Signup />} />
        </Route>
      </Routes>
      <ToastContainer />
    </>
  );
}

export default App;
