// Simple client-side i18n for English / Slovak with Database Synchronization
(function () {
    const translations = {
        en: {
            // Navbar
            nav_home: "Home",
            nav_draw: "Draw",
            nav_idk: "IDK",
            nav_my_teams: "My Teams",
            nav_facilities: "Facilities",
            nav_sign_in: "Sign in",
            nav_register: "Register",
            nav_players: "Players",
            fullscreen: "Fullscreen ⛶",
            leave: "Leave",
            teams: "Teams",

            // Common buttons / actions
            edit: "Edit",
            edit_metadata: "Edit metadata",
            remove: "Remove",
            cancel: "Cancel",
            create: "Create",
            save: "Save",
            save_changes: "Save Changes",
            choose: "Choose...",
            confirm_delete: "Are you sure?",

            // Profile
            anonymous: "Anonymous",
            logout: "Logout",
            inbox_title: "Inbox: Team Invitations",
            invite_text: "You've been invited to join <strong>{team}</strong> by {sender}.",
            accept: "Accept",
            decline: "Decline",
            no_invitations: "No new invitations.",
            switch_lang: "Switch language",
            settings: "Settings",

            // Profile edit
            ph_full_name: "Full Name",
            ph_nickname: "Nickname",
            email_label: "Email:",
            ph_dob: "Date of Birth",
            ph_role: "Role",
            goalkeeper: "Goalkeeper",
            defense: "Defense",
            center: "Center",
            attack: "Attack",
            left_handed: "Left handed (right hand lower)",

            // Home
            home_greeting: "Hello, ",
            home_guest: "Guest",
            home_subtitle: "Welcome to your sports statistics command center.",
            home_card_live: "Live Scores",
            home_card_live_desc: "Check real-time data for ongoing matches.",
            home_card_live_btn: "View Live",
            home_card_players: "Player Database",
            home_card_players_desc: "Search and analyze individual player performance.",
            home_card_players_btn: "Browse Players",
            home_card_compare: "Compare Teams",
            home_card_compare_desc: "Head-to-head statistics for upcoming games.",
            home_card_compare_btn: "Start Comparison",
            home_no_fav: "No Favorite Teams Added",
            home_no_fav_desc: "Follow a team to see their quick stats right here on your dashboard.",
            home_find_team: "Find a team to follow →",
            home_hero_title: "Deep Dive into Sports Data",
            home_hero_subtitle: "Professional grade statistics for enthusiasts and analysts alike.",
            home_hero_btn: "Create Free Account",

            // Facilities
            fac_create_new: "Create New Facility",
            fac_floor_type: "Floor Type",
            fac_floor_type_label: "Floor type:",
            ph_name: "Name",
            ph_street: "Street & street No.",
            ph_city: "City",
            fac_edit_title: "Edit {name}",
            wood: "Wood",
            rubber: "Rubber",
            other: "Other",

            // Teams
            team_create_new: "Create New Team",
            team_color_picker: "Color picker",
            team_home_facility: "Home Facility",
            team_search_user: "Search username...",
            team_invite: "Invite",
            team_new_match: "new match",
            team_edit_title: "Edit {name}",
            no_upcoming_matches: "No upcoming matches.",

            // New match
            match_vs: "vs",
            ph_opponent: "Opponent",
            match_roster: "roster",
            match_something: "something",

            // Auth
            auth_welcome_back: "Welcome Back",
            auth_username_or_email: "Username or Email",
            auth_username: "Username",
            auth_email: "Email",
            auth_password: "Password",
            auth_sign_in_btn: "Sign In",
            auth_sign_up_btn: "Sign Up",
            auth_create_account: "Create an Account",
            auth_new_here: "New here?",
            auth_sign_up_here: "Sign up here",
            auth_have_account: "Already have an account?",
            auth_sign_in_here: "Sign in here",

            // Match
            start: "Start",
            goal: "Goal",
            select: "Select",
            name: "Name",
            pts: "PTS"
        },
        sk: {
            // Navbar
            nav_home: "Domov",
            nav_draw: "Žreb",
            nav_idk: "Neviem",
            nav_my_teams: "Moje tímy",
            nav_facilities: "Štadióny",
            nav_sign_in: "Prihlásiť sa",
            nav_register: "Registrovať",
            nav_players: "Hráči",
            fullscreen: "Celá Obrazovka ⛶",
            leave: "Odisť",
            teams: "Tímy",

            // Common buttons / actions
            edit: "Upraviť",
            edit_metadata: "Upraviť údaje",
            remove: "Odstrániť",
            cancel: "Zrušiť",
            create: "Vytvoriť",
            save: "Uložiť",
            save_changes: "Uložiť zmeny",
            choose: "Vyberte...",
            confirm_delete: "Ste si istý?",

            // Profile
            anonymous: "Anonymný",
            logout: "Odhlásiť sa",
            inbox_title: "Schránka: Pozvánky do tímov",
            invite_text: "Boli ste pozvaný do tímu <strong>{team}</strong> od používateľa {sender}.",
            accept: "Prijať",
            decline: "Odmietnuť",
            no_invitations: "Žiadne nové pozvánky.",
            switch_lang: "Prepnúť jazyk",
            settings: "Nastavenia",

            // Profile edit
            ph_full_name: "Celé meno",
            ph_nickname: "Prezývka",
            email_label: "Email:",
            ph_dob: "Dátum narodenia",
            ph_role: "Pozícia",
            goalkeeper: "Brankár",
            defense: "Obranca",
            center: "Center",
            attack: "Útočník",
            left_handed: "Ľavák (pravá ruka dole)",

            // Home
            home_greeting: "Ahoj, ",
            home_guest: "Hosť",
            home_subtitle: "Vitajte vo vašom riadiacom centre športových štatistík.",
            home_card_live: "Live skóre",
            home_card_live_desc: "Sledujte dáta v reálnom čase z prebiehajúcich zápasov.",
            home_card_live_btn: "Zobraziť naživo",
            home_card_players: "Databáza hráčov",
            home_card_players_desc: "Vyhľadávajte a analyzujte výkony jednotlivých hráčov.",
            home_card_players_btn: "Prehliadať hráčov",
            home_card_compare: "Porovnať tímy",
            home_card_compare_desc: "Vzájomné štatistiky pre nadchádzajúce zápasy.",
            home_card_compare_btn: "Začať porovnanie",
            home_no_fav: "Žiadne obľúbené tímy",
            home_no_fav_desc: "Sledujte tím, aby sa jeho rýchle štatistiky zobrazili priamo na vašej nástenke.",
            home_find_team: "Nájsť tím →",
            home_hero_title: "Ponorte sa do športových dát",
            home_hero_subtitle: "Profesionálne štatistiky pre nadšencov aj analytikov.",
            home_hero_btn: "Vytvoriť účet zadarmo",

            // Facilities
            fac_create_new: "Pridať nový štadión",
            fac_floor_type: "Typ povrchu",
            fac_floor_type_label: "Typ povrchu:",
            ph_name: "Názov",
            ph_street: "Ulica a č. domu",
            ph_city: "Mesto",
            fac_edit_title: "Upraviť {name}",
            wood: "Drevo",
            rubber: "Guma",
            other: "Iný",

            // Teams
            team_create_new: "Vytvoriť nový tím",
            team_color_picker: "Výber farby",
            team_home_facility: "Domáci štadión",
            team_search_user: "Hľadať používateľa...",
            team_invite: "Pozvať",
            team_new_match: "nový zápas",
            team_edit_title: "Upraviť {name}",

            // New match
            match_vs: "vs",
            ph_opponent: "Súper",
            match_roster: "súpiska",
            match_something: "niečo",

            // Auth
            auth_welcome_back: "Vitajte späť",
            auth_username_or_email: "Používateľské meno alebo email",
            auth_username: "Používateľské meno",
            auth_email: "Email",
            auth_password: "Heslo",
            auth_sign_in_btn: "Prihlásiť sa",
            auth_sign_up_btn: "Zaregistrovať sa",
            auth_create_account: "Vytvoriť účet",
            auth_new_here: "Ste tu nový?",
            auth_sign_up_here: "Zaregistrujte sa tu",
            auth_have_account: "Už máte účet?",
            auth_sign_in_here: "Prihláste sa tu",

            // Match
            start: "Štart",
            goal: "Gól",
            select: "Vybrať",
            name: "Meno",
            pts: "B"
        }
    };

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    function interpolate(template, params) {
        return template.replace(/\{(\w+)\}/g, function (_, key) {
            return params[key] !== undefined ? escapeHtml(params[key]) : "{" + key + "}";
        });
    }

    function collectParams(el) {
        const params = {};
        for (const attr of el.attributes) {
            if (attr.name.startsWith("data-") &&
                attr.name !== "data-i18n" &&
                attr.name !== "data-i18n-placeholder" &&
                attr.name !== "data-i18n-title" &&
                attr.name !== "data-lang") {
                params[attr.name.substring(5)] = attr.value;
            }
        }
        return params;
    }

    function applyLanguage(lang) {
        if (!translations[lang]) lang = "en";
        const dict = translations[lang];

        document.querySelectorAll("[data-i18n]").forEach(function (el) {
            const key = el.getAttribute("data-i18n");
            if (!dict[key]) return;
            const text = interpolate(dict[key], collectParams(el));
            if (text.indexOf("<") !== -1) {
                el.innerHTML = text;
            } else {
                el.textContent = text;
            }
        });

        document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
            const key = el.getAttribute("data-i18n-placeholder");
            if (dict[key]) el.setAttribute("placeholder", dict[key]);
        });

        document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
            const key = el.getAttribute("data-i18n-title");
            if (dict[key]) el.setAttribute("title", dict[key]);
        });

        document.querySelectorAll(".lang-flag").forEach(function (el) {
            if (el.getAttribute("data-lang") === lang) {
                el.classList.add("active");
            } else {
                el.classList.remove("active");
            }
        });

        document.documentElement.setAttribute("lang", lang);
    }

    // UPDATED: Syncs language to the backend API if necessary
    function setLanguage(lang) {
        try {
            localStorage.setItem("preferredLang", lang);
        } catch (e) { /* storage unavailable, ignore */ }
        
        applyLanguage(lang);

        // Optional API integration: Send selection to the backend settings table
        fetch('/api/save-language', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ language: lang })
        }).catch(err => console.log("Not logged in or offline; language saved locally only."));
    }

    // UPDATED: Prioritizes Server-Injected data attribute over LocalStorage
    function getCurrentLanguage() {
        // Option A Check: Read from <html data-user-lang="sk"> injected by your backend
        const serverInjectedLang = document.documentElement.getAttribute("data-user-lang");
        if (serverInjectedLang && translations[serverInjectedLang]) {
            return serverInjectedLang;
        }

        try {
            return localStorage.getItem("preferredLang") || "en";
        } catch (e) {
            return "en";
        }
    }

    function t(key) {
        const lang = getCurrentLanguage();
        const dict = translations[lang] || translations.en;
        return dict[key] !== undefined ? dict[key] : (translations.en[key] || key);
    }

    window.I18n = {
        apply: applyLanguage,
        set: setLanguage,
        current: getCurrentLanguage,
        t: t
    };

    document.addEventListener("DOMContentLoaded", function () {
        applyLanguage(getCurrentLanguage());

        document.querySelectorAll(".lang-flag").forEach(function (el) {
            el.addEventListener("click", function (e) {
                e.preventDefault();
                setLanguage(el.getAttribute("data-lang"));
            });
        });
    });
})();