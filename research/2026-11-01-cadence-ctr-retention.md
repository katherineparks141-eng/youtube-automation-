# Posting cadence, CTR, and retention — research notes (Nov 1, 2026)

Backing research for the "Cadence target" section of `CLAUDE.md`.

## Upload frequency vs. growth

- Channel-growth studies (vidIQ aggregate data, channels sampled in the 1M–10M sub
  range) consistently show a step-change in growth rate around **~1 upload/week**.
  Channels posting less than ~1x/month essentially don't grow via the algorithm — they
  rely entirely on search/evergreen pull.
- Above 1/week, more frequency helps mostly by giving the algorithm more chances to
  test a channel with new viewers, not by compounding views linearly. 3–4x/week is a
  common "serious channel" cadence for faceless/automated niches specifically, because
  each video is cheap to produce once narration+visuals are automated (which is the
  case for both Forgotten & Found and Sleepy Meadow).
- **Conclusion applied in CLAUDE.md:** floor of 1/week per active channel (below this,
  don't bother), target of 3/week combined while testing two concepts, consider scaling
  to 3/week *each* only once production cost per video is proven low and one concept
  shows it's worth doubling down on.

## Timing

- Most "best time to post" advice (SocialPilot, Buffer, Sprout Social aggregate data,
  and YouTube Creator Insider commentary) agrees on: **weekday afternoons, 2–4 PM in
  the audience's time zone**, with Wednesday and Thursday the strongest single days for
  long-form on average.
- The mechanism matters more than the specific hour: YouTube needs time to show a new
  video to its initial test audience and gather signal (CTR, average view duration)
  *before* the main daily traffic wave hits. Practical rule: publish 1–2 hours before
  the channel's actual observed peak-traffic window (visible in Studio → Audience tab
  once there's data) rather than chasing a generic best time.
- This matters much more once a channel has an established audience with a real peak
  (roughly 10K+ subs) — below that, consistency of posting beats precision of timing.

## CTR / thumbnail practice

- Thumbnail A/B testing is officially supported in YouTube Studio and free — compare
  variants over a 24–48 hour window against the channel's own rolling-average CTR, not
  against a general "good CTR" number, since niche and channel size both move the
  baseline a lot.
- For kids' content specifically, multiple creator-economy sources (Tubular Labs
  commentary on top kids channels, YouTube's own Made-for-Kids creator guidance) note
  that **exaggerated/clickbait thumbnails perform worse on children's content** —
  parents (who make the click decision for younger kids) respond better to calm,
  accurate, trustworthy imagery. This is the opposite of the "shock face + bold text"
  norm in adult true-crime/history niches, which is why Sleepy Meadow and Forgotten &
  Found need genuinely different thumbnail styles even if both are AI-illustrated.

## Retention

- Average view duration / audience retention curve shape matters more to
  recommendations than raw watch time. Early-video drop-off (first 15–30 seconds) is
  the single biggest lever — a strong cold open matters more than mid-video pacing for
  getting the algorithm to keep testing a video with new viewers.
- Series/pillar structure (recommending the next video in the same pillar at the end)
  increases session watch time, which YouTube rewards at the channel level, not just
  the video level.
