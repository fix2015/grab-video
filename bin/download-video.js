#!/usr/bin/env node

'use strict';

const { program } = require('commander');
const { execSync, spawn } = require('child_process');
const path = require('path');
const chalk = require('chalk');

const pkg = require('../package.json');
const SCRIPTS_DIR = path.join(__dirname, '..', 'scripts');
const PYTHON_SCRIPT = path.join(SCRIPTS_DIR, 'download_video.py');

function checkPython() {
  try {
    execSync('python3 --version', { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

function checkYtDlp() {
  try {
    execSync('python3 -c "import yt_dlp"', { stdio: 'pipe', timeout: 10000 });
    return true;
  } catch {
    return false;
  }
}

function installDeps() {
  console.log(chalk.yellow('Installing yt-dlp...'));
  try {
    execSync('pip3 install yt-dlp', { stdio: 'inherit' });
    return true;
  } catch {
    console.error(chalk.red('Failed. Try manually: pip3 install yt-dlp'));
    return false;
  }
}

function ensureDeps() {
  if (!checkPython()) {
    console.error(chalk.red('Python 3 is required.'));
    console.error('  Install: https://www.python.org/downloads/');
    process.exit(1);
  }
  if (!checkYtDlp()) {
    if (!installDeps()) process.exit(1);
  }
}

function runPython(args) {
  const child = spawn('python3', [PYTHON_SCRIPT, ...args], {
    stdio: 'inherit',
    env: { ...process.env },
  });
  child.on('close', (code) => {
    process.exit(code || 0);
  });
}

program
  .name('get-video')
  .version(pkg.version)
  .description(
    'Download videos from YouTube, Instagram, TikTok, Facebook, Twitter, and 1000+ sites.\n\n' +
    'Powered by yt-dlp. Free and unlimited.'
  )
  .addHelpText('after', `
${chalk.bold('Examples:')}

  ${chalk.dim('# Download a YouTube video')}
  get-video "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

  ${chalk.dim('# Download Instagram reel')}
  get-video "https://www.instagram.com/reel/ABC123/"

  ${chalk.dim('# Download TikTok video')}
  get-video "https://www.tiktok.com/@user/video/123456"

  ${chalk.dim('# Choose quality')}
  get-video "https://youtube.com/watch?v=..." --quality 720

  ${chalk.dim('# Audio only (MP3)')}
  get-video "https://youtube.com/watch?v=..." --audio-only

  ${chalk.dim('# Save to specific folder')}
  get-video "https://youtube.com/watch?v=..." --output ./downloads/

  ${chalk.dim('# List available formats')}
  get-video "https://youtube.com/watch?v=..." --formats

  ${chalk.dim('# Download with subtitles')}
  get-video "https://youtube.com/watch?v=..." --subs

  ${chalk.dim('# Download entire playlist')}
  get-video "https://youtube.com/playlist?list=PLxxx"

${chalk.bold('Supported sites:')} YouTube, Instagram, TikTok, Facebook, Twitter/X,
  Telegram, Reddit, Vimeo, Twitch, Dailymotion, SoundCloud, and 1000+ more.
  Full list: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
`);

// ---- SETUP ----
program
  .command('setup')
  .description('Check Python and install yt-dlp')
  .action(() => {
    console.log(chalk.bold('\nget-video setup\n'));

    if (!checkPython()) {
      console.error(chalk.red('  Python 3 not found.'));
      process.exit(1);
    }
    console.log(chalk.green('  Python 3 found'));

    if (!checkYtDlp()) {
      if (!installDeps()) process.exit(1);
    } else {
      console.log(chalk.green('  yt-dlp installed'));
    }

    console.log(chalk.bold('\n  Ready! Try: get-video "https://youtube.com/watch?v=..."\n'));
  });

// ---- UPDATE ----
program
  .command('update')
  .description('Update yt-dlp to the latest version')
  .action(() => {
    console.log(chalk.yellow('Updating yt-dlp...'));
    try {
      execSync('pip3 install --upgrade yt-dlp', { stdio: 'inherit' });
      console.log(chalk.green('\n  yt-dlp updated!\n'));
    } catch {
      console.error(chalk.red('Failed. Try: pip3 install --upgrade yt-dlp'));
    }
  });

// ---- SITES ----
program
  .command('sites')
  .description('List popular supported sites')
  .action(() => {
    console.log(`
${chalk.bold('Supported sites (1000+):')}

  ${chalk.cyan('Video:')}
    YouTube, YouTube Music, YouTube Shorts
    Instagram (posts, reels, stories)
    TikTok
    Facebook, Facebook Reels
    Twitter / X
    Telegram
    Reddit
    Vimeo
    Twitch (clips, VODs)
    Dailymotion
    Bilibili
    Rumble
    Odysee

  ${chalk.cyan('Audio:')}
    SoundCloud
    Bandcamp
    Mixcloud
    Spotify (metadata only)

  ${chalk.cyan('Other:')}
    LinkedIn
    Pinterest
    Tumblr
    VK
    Weibo
    Niconico
    Crunchyroll

  Full list: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
`);
  });

// ---- DEFAULT: download ----
program
  .argument('[url]', 'Video URL to download')
  .option('-q, --quality <res>', 'Max video quality: 360, 480, 720, 1080, 1440, 2160, best', 'best')
  .option('-o, --output <path>', 'Output directory or file path', '.')
  .option('-a, --audio-only', 'Download audio only (MP3)')
  .option('-f, --formats', 'List available formats for the URL')
  .option('-s, --subs', 'Download subtitles if available')
  .option('--subs-lang <lang>', 'Subtitle language code (e.g. en, es, fr)', 'en')
  .option('--playlist', 'Download entire playlist')
  .option('--thumbnail', 'Also download thumbnail image')
  .option('--metadata', 'Show video metadata (title, duration, etc.) without downloading')
  .option('--limit-rate <rate>', 'Limit download speed (e.g. 1M, 500K)')
  .option('--proxy <url>', 'Use proxy for download')
  .option('--cookies <file>', 'Path to cookies file (for private/age-restricted videos)')
  .action((url, opts) => {
    if (!url) {
      program.help();
      return;
    }

    ensureDeps();

    const args = ['--url', url];

    if (opts.formats) {
      args.push('--formats');
      runPython(args);
      return;
    }

    if (opts.metadata) {
      args.push('--metadata');
      runPython(args);
      return;
    }

    args.push('--quality', opts.quality);
    args.push('--output', path.resolve(opts.output));

    if (opts.audioOnly) args.push('--audio-only');
    if (opts.subs) args.push('--subs', '--subs-lang', opts.subsLang);
    if (opts.playlist) args.push('--playlist');
    if (opts.thumbnail) args.push('--thumbnail');
    if (opts.limitRate) args.push('--limit-rate', opts.limitRate);
    if (opts.proxy) args.push('--proxy', opts.proxy);
    if (opts.cookies) args.push('--cookies', path.resolve(opts.cookies));

    runPython(args);
  });

program.parse(process.argv);
