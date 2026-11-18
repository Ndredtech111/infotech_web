<?php
/**
 * Copy this file to config.php on the server and fill in the real values.
 * NEVER commit config.php (it is listed in .gitignore).
 */
return [
    // MySQL details from cPanel > MySQL Databases
    'db' => [
        'host' => 'localhost',
        'name' => 'cpanelprefix_ndr',
        'user' => 'cpanelprefix_ndruser',
        'pass' => 'CHANGE_ME_TO_A_STRONG_PASSWORD',
    ],

    // Who receives each enquiry
    'mail' => [
        'to'   => ['hr@ndrinfotech.com', 'dineshreddyvari@ndrinfotech.com'],
        'from' => 'no-reply@ndrinfotech.com',   // must be an address on your own domain
    ],

    // Websites allowed to call this API
    'allowed_origins' => [
        'https://www.ndrinfotech.com',
        'https://ndrinfotech.com',
    ],
];
