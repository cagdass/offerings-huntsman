import React from "react";
import {Route, IndexRoute} from "react-router";
import MainHome from "./components/main_home";
import DepartmentList from "./components/department_list";
import NoMatch from "components/no_match";

const routes = (
    <Route path="/" component={MainHome}>
        <IndexRoute component={DepartmentList}/>
        <Route path="departments" component={DepartmentList}>
        </Route>
        <Route path="*" component={NoMatch}/>
    </Route>
);

export default routes;