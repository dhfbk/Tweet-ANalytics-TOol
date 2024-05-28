<template>
<!--  <img alt="Vue logo" src="./assets/logo.png">-->
<!--    <h1 class="display-1">Ciao</h1>-->
<!--    <router-view msg="Ciao a tutti"/>-->

    <div id="app">
        <!--<nav class="navbar bg-dark" data-bs-theme="dark">   src="./assets/Logo.png"-->
        <!--sfondo: bg-light colore testo: navbar-light-->

        <!--    <nav class="navbar fixed-top bg-light navbar-toggleable-md">-->

        <!--ombreggiatura: shadow-sm p-3 mb-5 bg-body rounded-->
        <nav
            id="nav"
            class="navbar navbar-expand-md bg-light navbar-light navbar-toggleable-md shadow-sm p-3 mb-5 bg-body rounded"
        >
            <div class="container-fluid">
                <!--
                <div class="d-flex flex-column w-100">
                    -->
                <router-link class="navbar-brand" to="/">
                    <img src="./assets/Logo.jpg" alt="Logo" style="width: 150px" />
                </router-link>
                <!--menu ad hamburger-->
                <button
                    class="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapsibleNavbar"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>

                <!-- Navbar links -->
                <div
                    class="collapse navbar-collapse display: inline-block"
                    id="collapsibleNavbar"
                >
                    <div class="d-flex flex-column w-100">
                        <!--
                          PROBLEMA: mx-auto se aggiunto lo centra nel drop down ma anche fuori -->
<!--                        <ul class="navbar-nav py-2 justify-content-end">-->
<!--                            <li class="nav-item dropdown">-->
<!--                                <a-->
<!--                                    class="nav-link dropdown-toggle"-->
<!--                                    href="#"-->
<!--                                    id="navbarDropdownMenuLink"-->
<!--                                    role="button"-->
<!--                                    data-bs-toggle="dropdown"-->
<!--                                    aria-expanded="false"-->
<!--                                >-->
<!--                                    <i class="bi bi-globe"></i> {{ value }}-->
<!--                                </a>-->
<!--                                <ul-->
<!--                                    class="dropdown-menu dropdown-menu-end"-->
<!--                                    aria-labelledby="navbarDropdownMenuLink"-->
<!--                                >-->
<!--                                    <li v-for="option in options" :key="option">-->
<!--                                        <a class="dropdown-item" @click="value = option">{{-->
<!--                                                option-->
<!--                                            }}</a>-->
<!--                                    </li>-->
<!--                                </ul>-->
<!--                            </li>-->
<!--                        </ul>-->
                        <!--2 riga-->
                        <div id="secondaRiga" class="navbar-nav justify-content-center">
                            <router-link to="/Know_more" class="nav-item nav-link"
                            >1. Learn more</router-link>
                            <router-link to="/Test_yourself" class="nav-item nav-link"
                            >2. Challenge yourself</router-link>
                            <router-link to="/Hands_on" class="nav-item nav-link"
                            >3. Analyse</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
        <router-view msg="Ciao"/>
    </div>
</template>

<script>

export default {
  name: 'App'
}
</script>

<style>
/*#app {*/
/*  font-family: Avenir, Helvetica, Arial, sans-serif;*/
/*  -webkit-font-smoothing: antialiased;*/
/*  -moz-osx-font-smoothing: grayscale;*/
/*  text-align: center;*/
/*  color: #2c3e50;*/
/*  margin-top: 60px;*/
/*}*/

#nav {
    padding: 30px;
}

#nav a {
    font-family: "Rajdhani", sans-serif !important;
    font-weight: 500;
    /*font-size: 16px;*/
    color: #000000;
}

#nav {
    padding: 30px;
    text-align: center;
}

#nav a.router-link-exact-active {
    color: #ec6362 !important;
    font-weight: 600;
    /*background: #ec6362;*/
    border-radius: 0.5rem;
}

</style>
