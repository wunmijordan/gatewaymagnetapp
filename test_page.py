{% extends "base.html" %}
{% load form_tags %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="page page-center">
  <div class="container-tight py-4">
    <form method="post" class="card card-md bg-dark text-white border-0 shadow-sm">
      {% csrf_token %}
      <div class="card-body">
        <h2 class="card-title text-center mb-4 text-white">Sign In</h2>

        {% if form.errors %}
          <div class="alert alert-danger">
            Invalid username or password.
          </div>
        {% endif %}

        <div class="mb-3">
          <label for="{{ form.username.id_for_label }}" class="form-label text-white">Username</label>
          {{ form.username|add_class:"form-control bg-dark text-white border-secondary" }}
        </div>

        <div class="mb-3">
          <label for="{{ form.password.id_for_label }}" class="form-label text-white">Password</label>
          {{ form.password|add_class:"form-control bg-dark text-white border-secondary" }}
        </div>

        <div class="form-footer mt-4">
          <button type="submit" class="btn btn-primary w-100">Sign In</button>
        </div>
      </div>
    </form>
  </div>
</div>
{% endblock %}






{% load static %}
{% load pwa %}
{% load user_avatar_tags %}
{% load guest_avatar_tags %}
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}Gateway Magnet{% endblock %}</title>
    {% progressive_web_app_meta %}
    <link rel="manifest" href="{% static 'manifest.json' %}">
    <meta name="theme-color" content="#000000">
    <link rel="apple-touch-icon" href="{% static 'icons/icon-192x192.png' %}">
    
    <!-- Bootstrap 5.3 CSS (or your Tabler CSS) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/@tabler/core@latest/dist/css/tabler.min.css" rel="stylesheet" />
    <link rel="stylesheet" href="https://unpkg.com/@tabler/icons-webfont/tabler-icons.min.css">

    <link href="{% static 'css/custom.css' %}" rel="stylesheet" />

  <head>
  <body>
  




    <div class="page page-center">
      <div class="container container-tight py-4">
        <div class="text-center mb-4">
          <!-- BEGIN NAVBAR LOGO -->
          <a href="{% url 'dashboard' %}" aria-label="Gateway Nation" class="navbar-brand navbar-brand-autodark">
            <img src="{% static 'images/church_logo.png' %}" alt="Logo" style="width: 120px; height: 120px;">
          </a>
          <!-- END NAVBAR LOGO -->
        </div>
        <div class="card card-md">
          <div class="card-body">
            <h2 class="h2 text-center mb-4">Login to your account</h2>
            <form method="post">
              {% csrf_token %}
              
              <div class="mb-3">                
                <label for="{{ form.username.id_for_label }}" class="form-label">Username</label>
                <input type="text" class="form-control" placeholder="magnetmember" autocomplete="on" name="username">
              </div>
              <div class="mb-2">
                <label for="{{ form.password.id_for_label }}" class="form-label">
                  Password
                  <span class="form-label-description">
                    <a href="tel:+2349011099449">I forgot my Password</a>
                  </span>
                </label>
                <div class="input-group input-group-flat">
                  <input type="password" id="passwordInput" class="form-control" placeholder="mypxxxword" autocomplete="current-password">
                  <span class="input-group-text">
                    <a href="#" class="link-secondary toggle-password" data-bs-toggle="tooltip" aria-label="Show password" data-bs-original-title="Show password">
                      <svg id="eyeIcon" xmlns="http://www.w3.org/2000/svg" class="icon icon-1 transition" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />
                        <path d="M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6" />
                      </svg>
                    </a>
                  </span>
                </div>
              </div>
              <div class="mb-2">
                <label class="form-check">
                  <input type="checkbox" name="remember_me" class="form-check-input">
                  <span class="form-check-label">Remember me on this device</span>
                </label>
              </div>
              <div class="form-footer">
                <button type="submit" class="btn btn-primary w-100">Sign in</button>
              </div>
            </form>
          </div>
        </div>
        <div class="text-center text-secondary mt-3">Any trouble signing in? <a href="tel:+2349011099449" tabindex="-1">Contact Admin</a></div>
      </div>
    </div>


    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>


    <!-- Your custom JS -->
    <script src="{% static 'js/custom.js' %}"></script>
  </body>
</html>
























          <div class="card card-md mb-4">
            <div class="card-header">
            <h4 class="card-title">New Report</h4>
            </div>
            <div class="card-body">
              <div class="col-md-6 mb-3">
                <label class="form-label">Report Date</label>
                <input type="date" name="report_date" class="form-control" value="{{ today|date:'Y-m-d' }}" required>
              </div>

              <div class="col-md-6 mb-3">
                <label class="form-label">Service Attendance</label>
                <div class="form-check">
                <input class="form-check-input" type="checkbox" id="serviceSunday" name="service_sunday">
                <label class="form-check-label" for="serviceSunday">Sunday Service</label>
                </div>
                <div class="form-check">
                <input class="form-check-input" type="checkbox" id="serviceMidweek" name="service_midweek">
                <label class="form-check-label" for="serviceMidweek">Mid-Week Service</label>
                </div>
              </div>

              <div class="col-md-12 mb-3">
                <label class="form-label">Follow-Up Note</label>
                <textarea name="note" class="form-control" id="id_note" rows="4" placeholder="Enter your follow-up report note" required></textarea>
              </div>
            </div>
          </div>

          <div class="modal-footer mt-4 d-flex gap-2">
            <button type="submit" class="btn btn-primary">
              <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-file-isr">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                <path d="M15 3v4a1 1 0 0 0 1 1h4" /><path d="M15 3v4a1 1 0 0 0 1 1h4" /><path d="M6 8v-3a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-7" /><path d="M3 15l3 -3l3 3" />
              </svg>
              Submit Report
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close">
              <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-cancel">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                <path d="M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" /><path d="M18.364 5.636l-12.728 12.728" />
              </svg>
              Cancel
            </button>
          </div>
        </div>
        

      </form>
    </div>
  </div>
</div>




















<div class="col-lg-6">
                <div class="card">
                  <div class="card-body">
                    <h3 class="card-title">Traffic summary</h3>
                    <div id="chart-mentions" class="position-relative chart-lg" style="min-height: 240px;"><div id="apexchartsfndk2ib5" class="apexcharts-canvas apexchartsfndk2ib5 apexcharts-theme-" style="width: 738px; height: 240px;"><svg id="SvgjsSvg5589" width="738" height="240" xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.dev" class="apexcharts-svg apexcharts-zoomable" xmlns:data="ApexChartsNS" transform="translate(0, 0)"><foreignObject x="0" y="0" width="738" height="240"><div class="apexcharts-legend" xmlns="http://www.w3.org/1999/xhtml" style="max-height: 120px;"></div><style type="text/css">
      .apexcharts-flip-y {
        transform: scaleY(-1) translateY(-100%);
        transform-origin: top;
        transform-box: fill-box;
      }
      .apexcharts-flip-x {
        transform: scaleX(-1);
        transform-origin: center;
        transform-box: fill-box;
      }
      .apexcharts-legend {
        display: flex;
        overflow: auto;
        padding: 0 10px;
      }
      .apexcharts-legend.apx-legend-position-bottom, .apexcharts-legend.apx-legend-position-top {
        flex-wrap: wrap
      }
      .apexcharts-legend.apx-legend-position-right, .apexcharts-legend.apx-legend-position-left {
        flex-direction: column;
        bottom: 0;
      }
      .apexcharts-legend.apx-legend-position-bottom.apexcharts-align-left, .apexcharts-legend.apx-legend-position-top.apexcharts-align-left, .apexcharts-legend.apx-legend-position-right, .apexcharts-legend.apx-legend-position-left {
        justify-content: flex-start;
      }
      .apexcharts-legend.apx-legend-position-bottom.apexcharts-align-center, .apexcharts-legend.apx-legend-position-top.apexcharts-align-center {
        justify-content: center;
      }
      .apexcharts-legend.apx-legend-position-bottom.apexcharts-align-right, .apexcharts-legend.apx-legend-position-top.apexcharts-align-right {
        justify-content: flex-end;
      }
      .apexcharts-legend-series {
        cursor: pointer;
        line-height: normal;
        display: flex;
        align-items: center;
      }
      .apexcharts-legend-text {
        position: relative;
        font-size: 14px;
      }
      .apexcharts-legend-text *, .apexcharts-legend-marker * {
        pointer-events: none;
      }
      .apexcharts-legend-marker {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        margin-right: 1px;
      }

      .apexcharts-legend-series.apexcharts-no-click {
        cursor: auto;
      }
      .apexcharts-legend .apexcharts-hidden-zero-series, .apexcharts-legend .apexcharts-hidden-null-series {
        display: none !important;
      }
      .apexcharts-inactive-legend {
        opacity: 0.45;
      }</style></foreignObject><g id="SvgjsG5609" class="apexcharts-datalabels-group" transform="translate(0, 0) scale(1)"></g><g id="SvgjsG5610" class="apexcharts-datalabels-group" transform="translate(0, 0) scale(1)"></g><g id="SvgjsG5884" class="apexcharts-yaxis" rel="0" transform="translate(15.41357421875, 0)"><g id="SvgjsG5885" class="apexcharts-yaxis-texts-g"><text id="SvgjsText5887" font-family="inherit" x="4" y="13.666666666666666" text-anchor="end" dominant-baseline="auto" font-size="11px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-yaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5888">100</tspan><title>100</title></text><text id="SvgjsText5890" font-family="inherit" x="4" y="53.86666666666667" text-anchor="end" dominant-baseline="auto" font-size="11px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-yaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5891">80</tspan><title>80</title></text><text id="SvgjsText5893" font-family="inherit" x="4" y="94.06666666666666" text-anchor="end" dominant-baseline="auto" font-size="11px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-yaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5894">60</tspan><title>60</title></text><text id="SvgjsText5896" font-family="inherit" x="4" y="134.26666666666665" text-anchor="end" dominant-baseline="auto" font-size="11px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-yaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5897">40</tspan><title>40</title></text><text id="SvgjsText5899" font-family="inherit" x="4" y="174.46666666666664" text-anchor="end" dominant-baseline="auto" font-size="11px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-yaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5900">20</tspan><title>20</title></text><text id="SvgjsText5902" font-family="inherit" x="4" y="214.66666666666663" text-anchor="end" dominant-baseline="auto" font-size="11px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-yaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5903">0</tspan><title>0</title></text></g></g><g id="SvgjsG5591" class="apexcharts-inner apexcharts-graphical" transform="translate(39.25505235460069, 10)"><defs id="SvgjsDefs5590"><linearGradient id="SvgjsLinearGradient5595" x1="0" y1="0" x2="0" y2="1"><stop id="SvgjsStop5596" stop-opacity="0.4" stop-color="rgba(216,227,240,0.4)" offset="0"></stop><stop id="SvgjsStop5597" stop-opacity="0.5" stop-color="rgba(190,209,230,0.5)" offset="1"></stop><stop id="SvgjsStop5598" stop-opacity="0.5" stop-color="rgba(190,209,230,0.5)" offset="1"></stop></linearGradient><clipPath id="gridRectMaskfndk2ib5"><rect id="SvgjsRect5606" width="688.9034695095486" height="201" x="0" y="0" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fff"></rect></clipPath><clipPath id="gridRectBarMaskfndk2ib5"><rect id="SvgjsRect5607" width="712.58642578125" height="205" x="-11.841478135850695" y="-2" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fff"></rect></clipPath><clipPath id="gridRectMarkerMaskfndk2ib5"><rect id="SvgjsRect5608" width="688.9034695095486" height="201" x="0" y="0" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fff"></rect></clipPath><clipPath id="forecastMaskfndk2ib5"></clipPath><clipPath id="nonForecastMaskfndk2ib5"></clipPath></defs><rect id="SvgjsRect5599" width="9.568103743188175" height="201" x="645.4318905112184" y="0" rx="0" ry="0" opacity="1" stroke-width="0" stroke-dasharray="3" fill="url(#SvgjsLinearGradient5595)" class="apexcharts-xcrosshairs" y2="201" filter="none" fill-opacity="0.9" x1="645.4318905112184" x2="645.4318905112184"></rect><line id="SvgjsLine5848" x1="57.40862245912905" y1="201" x2="57.40862245912905" y2="207" stroke="#e0e0e0" stroke-dasharray="0" stroke-linecap="butt" class="apexcharts-xaxis-tick"></line><line id="SvgjsLine5850" x1="191.3620748637635" y1="201" x2="191.3620748637635" y2="207" stroke="#e0e0e0" stroke-dasharray="0" stroke-linecap="butt" class="apexcharts-xaxis-tick"></line><line id="SvgjsLine5852" x1="325.31552726839794" y1="201" x2="325.31552726839794" y2="207" stroke="#e0e0e0" stroke-dasharray="0" stroke-linecap="butt" class="apexcharts-xaxis-tick"></line><line id="SvgjsLine5854" x1="478.40518715940874" y1="201" x2="478.40518715940874" y2="207" stroke="#e0e0e0" stroke-dasharray="0" stroke-linecap="butt" class="apexcharts-xaxis-tick"></line><line id="SvgjsLine5856" x1="631.4948470504198" y1="201" x2="631.4948470504198" y2="207" stroke="#e0e0e0" stroke-dasharray="0" stroke-linecap="butt" class="apexcharts-xaxis-tick"></line><g id="SvgjsG5843" class="apexcharts-grid"><g id="SvgjsG5844" class="apexcharts-gridlines-horizontal"><line id="SvgjsLine5858" x1="-9.841478135850695" y1="40.2" x2="698.7449476453993" y2="40.2" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine5859" x1="-9.841478135850695" y1="80.4" x2="698.7449476453993" y2="80.4" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine5860" x1="-9.841478135850695" y1="120.60000000000001" x2="698.7449476453993" y2="120.60000000000001" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine5861" x1="-9.841478135850695" y1="160.8" x2="698.7449476453993" y2="160.8" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line></g><g id="SvgjsG5845" class="apexcharts-gridlines-vertical"><line id="SvgjsLine5847" x1="57.40862245912905" y1="0" x2="57.40862245912905" y2="201" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine5849" x1="191.3620748637635" y1="0" x2="191.3620748637635" y2="201" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine5851" x1="325.31552726839794" y1="0" x2="325.31552726839794" y2="201" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine5853" x1="478.40518715940874" y1="0" x2="478.40518715940874" y2="201" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine5855" x1="631.4948470504198" y1="0" x2="631.4948470504198" y2="201" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line></g><line id="SvgjsLine5864" x1="0" y1="201" x2="688.9034695095486" y2="201" stroke="transparent" stroke-dasharray="0" stroke-linecap="butt"></line><line id="SvgjsLine5863" x1="0" y1="1" x2="0" y2="201" stroke="transparent" stroke-dasharray="0" stroke-linecap="butt"></line></g><g id="SvgjsG5846" class="apexcharts-grid-borders"><line id="SvgjsLine5857" x1="-9.841478135850695" y1="0" x2="698.7449476453993" y2="0" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line><line id="SvgjsLine5862" x1="-9.841478135850695" y1="201" x2="698.7449476453993" y2="201" stroke="#e0e0e0" stroke-dasharray="4" stroke-linecap="butt" class="apexcharts-gridline"></line></g><g id="SvgjsG5611" class="apexcharts-bar-series apexcharts-plot-series"><g id="SvgjsG5612" class="apexcharts-series" seriesName="Web" rel="1" data:realIndex="0"><path id="SvgjsPath5616" d="M -4.784051871594087 201.001 L -4.784051871594087 198.991 C -4.784051871594087 198.991 -4.784051871594087 198.991 -4.784051871594087 198.991 L 4.784051871594087 198.991 C 4.784051871594087 198.991 4.784051871594087 198.991 4.784051871594087 198.991 L 4.784051871594087 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M -4.784051871594087 201.001 L -4.784051871594087 198.991 C -4.784051871594087 198.991 -4.784051871594087 198.991 -4.784051871594087 198.991 L 4.784051871594087 198.991 C 4.784051871594087 198.991 4.784051871594087 198.991 4.784051871594087 198.991 L 4.784051871594087 201.001 z " pathFrom="M -4.784051871594087 201.001 L -4.784051871594087 201.001 L 4.784051871594087 201.001 L 4.784051871594087 201.001 L 4.784051871594087 201.001 L 4.784051871594087 201.001 L 4.784051871594087 201.001 L -4.784051871594087 201.001 z" cy="198.99" cx="4.784051871594087" j="0" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5618" d="M 0 201" fill="none" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 14.352155614782262 201.001 L NaN NaN C NaN NaN 14.352155614782262 201.001 14.352155614782262 201.001 L 23.920259357970437 201.001 C 23.920259357970437 201.001 NaN NaN NaN NaN L 23.920259357970437 201.001 z " pathFrom="M 14.352155614782262 201.001 L 14.352155614782262 201.001 L 23.920259357970437 201.001 L 23.920259357970437 201.001 L 23.920259357970437 201.001 L 23.920259357970437 201.001 L 23.920259357970437 201.001 L 14.352155614782262 201.001 z" cy="201" cx="23.920259357970437" j="1" val="0" barHeight="0" barWidth="9.568103743188175"></path><path id="SvgjsPath5620" d="M 0 201" fill="none" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 33.48836310115861 201.001 L NaN NaN C NaN NaN 33.48836310115861 201.001 33.48836310115861 201.001 L 43.05646684434679 201.001 C 43.05646684434679 201.001 NaN NaN NaN NaN L 43.05646684434679 201.001 z " pathFrom="M 33.48836310115861 201.001 L 33.48836310115861 201.001 L 43.05646684434679 201.001 L 43.05646684434679 201.001 L 43.05646684434679 201.001 L 43.05646684434679 201.001 L 43.05646684434679 201.001 L 33.48836310115861 201.001 z" cy="201" cx="43.05646684434679" j="2" val="0" barHeight="0" barWidth="9.568103743188175"></path><path id="SvgjsPath5622" d="M 0 201" fill="none" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 52.62457058753496 201.001 L NaN NaN C NaN NaN 52.62457058753496 201.001 52.62457058753496 201.001 L 62.192674330723136 201.001 C 62.192674330723136 201.001 NaN NaN NaN NaN L 62.192674330723136 201.001 z " pathFrom="M 52.62457058753496 201.001 L 52.62457058753496 201.001 L 62.192674330723136 201.001 L 62.192674330723136 201.001 L 62.192674330723136 201.001 L 62.192674330723136 201.001 L 62.192674330723136 201.001 L 52.62457058753496 201.001 z" cy="201" cx="62.192674330723136" j="3" val="0" barHeight="0" barWidth="9.568103743188175"></path><path id="SvgjsPath5624" d="M 0 201" fill="none" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 71.76077807391131 201.001 L NaN NaN C NaN NaN 71.76077807391131 201.001 71.76077807391131 201.001 L 81.32888181709949 201.001 C 81.32888181709949 201.001 NaN NaN NaN NaN L 81.32888181709949 201.001 z " pathFrom="M 71.76077807391131 201.001 L 71.76077807391131 201.001 L 81.32888181709949 201.001 L 81.32888181709949 201.001 L 81.32888181709949 201.001 L 81.32888181709949 201.001 L 81.32888181709949 201.001 L 71.76077807391131 201.001 z" cy="201" cx="81.32888181709949" j="4" val="0" barHeight="0" barWidth="9.568103743188175"></path><path id="SvgjsPath5626" d="M 90.89698556028766 201.001 L 90.89698556028766 198.991 C 90.89698556028766 198.991 90.89698556028766 198.991 90.89698556028766 198.991 L 100.46508930347584 198.991 C 100.46508930347584 198.991 100.46508930347584 198.991 100.46508930347584 198.991 L 100.46508930347584 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 90.89698556028766 201.001 L 90.89698556028766 198.991 C 90.89698556028766 198.991 90.89698556028766 198.991 90.89698556028766 198.991 L 100.46508930347584 198.991 C 100.46508930347584 198.991 100.46508930347584 198.991 100.46508930347584 198.991 L 100.46508930347584 201.001 z " pathFrom="M 90.89698556028766 201.001 L 90.89698556028766 201.001 L 100.46508930347584 201.001 L 100.46508930347584 201.001 L 100.46508930347584 201.001 L 100.46508930347584 201.001 L 100.46508930347584 201.001 L 90.89698556028766 201.001 z" cy="198.99" cx="100.46508930347584" j="5" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5628" d="M 110.03319304666401 201.001 L 110.03319304666401 198.991 C 110.03319304666401 198.991 110.03319304666401 198.991 110.03319304666401 198.991 L 119.60129678985219 198.991 C 119.60129678985219 198.991 119.60129678985219 198.991 119.60129678985219 198.991 L 119.60129678985219 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 110.03319304666401 201.001 L 110.03319304666401 198.991 C 110.03319304666401 198.991 110.03319304666401 198.991 110.03319304666401 198.991 L 119.60129678985219 198.991 C 119.60129678985219 198.991 119.60129678985219 198.991 119.60129678985219 198.991 L 119.60129678985219 201.001 z " pathFrom="M 110.03319304666401 201.001 L 110.03319304666401 201.001 L 119.60129678985219 201.001 L 119.60129678985219 201.001 L 119.60129678985219 201.001 L 119.60129678985219 201.001 L 119.60129678985219 201.001 L 110.03319304666401 201.001 z" cy="198.99" cx="119.60129678985219" j="6" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5630" d="M 0 201" fill="none" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 129.16940053304035 201.001 L NaN NaN C NaN NaN 129.16940053304035 201.001 129.16940053304035 201.001 L 138.73750427622852 201.001 C 138.73750427622852 201.001 NaN NaN NaN NaN L 138.73750427622852 201.001 z " pathFrom="M 129.16940053304035 201.001 L 129.16940053304035 201.001 L 138.73750427622852 201.001 L 138.73750427622852 201.001 L 138.73750427622852 201.001 L 138.73750427622852 201.001 L 138.73750427622852 201.001 L 129.16940053304035 201.001 z" cy="201" cx="138.73750427622852" j="7" val="0" barHeight="0" barWidth="9.568103743188175"></path><path id="SvgjsPath5632" d="M 0 201" fill="none" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 148.3056080194167 201.001 L NaN NaN C NaN NaN 148.3056080194167 201.001 148.3056080194167 201.001 L 157.87371176260487 201.001 C 157.87371176260487 201.001 NaN NaN NaN NaN L 157.87371176260487 201.001 z " pathFrom="M 148.3056080194167 201.001 L 148.3056080194167 201.001 L 157.87371176260487 201.001 L 157.87371176260487 201.001 L 157.87371176260487 201.001 L 157.87371176260487 201.001 L 157.87371176260487 201.001 L 148.3056080194167 201.001 z" cy="201" cx="157.87371176260487" j="8" val="0" barHeight="0" barWidth="9.568103743188175"></path><path id="SvgjsPath5634" d="M 0 201" fill="none" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 167.44181550579304 201.001 L NaN NaN C NaN NaN 167.44181550579304 201.001 167.44181550579304 201.001 L 177.00991924898122 201.001 C 177.00991924898122 201.001 NaN NaN NaN NaN L 177.00991924898122 201.001 z " pathFrom="M 167.44181550579304 201.001 L 167.44181550579304 201.001 L 177.00991924898122 201.001 L 177.00991924898122 201.001 L 177.00991924898122 201.001 L 177.00991924898122 201.001 L 177.00991924898122 201.001 L 167.44181550579304 201.001 z" cy="201" cx="177.00991924898122" j="9" val="0" barHeight="0" barWidth="9.568103743188175"></path><path id="SvgjsPath5636" d="M 186.5780229921694 201.001 L 186.5780229921694 196.981 C 186.5780229921694 196.981 186.5780229921694 196.981 186.5780229921694 196.981 L 196.14612673535757 196.981 C 196.14612673535757 196.981 196.14612673535757 196.981 196.14612673535757 196.981 L 196.14612673535757 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 186.5780229921694 201.001 L 186.5780229921694 196.981 C 186.5780229921694 196.981 186.5780229921694 196.981 186.5780229921694 196.981 L 196.14612673535757 196.981 C 196.14612673535757 196.981 196.14612673535757 196.981 196.14612673535757 196.981 L 196.14612673535757 201.001 z " pathFrom="M 186.5780229921694 201.001 L 186.5780229921694 201.001 L 196.14612673535757 201.001 L 196.14612673535757 201.001 L 196.14612673535757 201.001 L 196.14612673535757 201.001 L 196.14612673535757 201.001 L 186.5780229921694 201.001 z" cy="196.98" cx="196.14612673535757" j="10" val="2" barHeight="4.02" barWidth="9.568103743188175"></path><path id="SvgjsPath5638" d="M 205.71423047854574 201.001 L 205.71423047854574 176.881 C 205.71423047854574 176.881 205.71423047854574 176.881 205.71423047854574 176.881 L 215.28233422173392 176.881 C 215.28233422173392 176.881 215.28233422173392 176.881 215.28233422173392 176.881 L 215.28233422173392 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 205.71423047854574 201.001 L 205.71423047854574 176.881 C 205.71423047854574 176.881 205.71423047854574 176.881 205.71423047854574 176.881 L 215.28233422173392 176.881 C 215.28233422173392 176.881 215.28233422173392 176.881 215.28233422173392 176.881 L 215.28233422173392 201.001 z " pathFrom="M 205.71423047854574 201.001 L 205.71423047854574 201.001 L 215.28233422173392 201.001 L 215.28233422173392 201.001 L 215.28233422173392 201.001 L 215.28233422173392 201.001 L 215.28233422173392 201.001 L 205.71423047854574 201.001 z" cy="176.88" cx="215.28233422173392" j="11" val="12" barHeight="24.12" barWidth="9.568103743188175"></path><path id="SvgjsPath5640" d="M 224.8504379649221 201.001 L 224.8504379649221 190.951 C 224.8504379649221 190.951 224.8504379649221 190.951 224.8504379649221 190.951 L 234.41854170811027 190.951 C 234.41854170811027 190.951 234.41854170811027 190.951 234.41854170811027 190.951 L 234.41854170811027 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 224.8504379649221 201.001 L 224.8504379649221 190.951 C 224.8504379649221 190.951 224.8504379649221 190.951 224.8504379649221 190.951 L 234.41854170811027 190.951 C 234.41854170811027 190.951 234.41854170811027 190.951 234.41854170811027 190.951 L 234.41854170811027 201.001 z " pathFrom="M 224.8504379649221 201.001 L 224.8504379649221 201.001 L 234.41854170811027 201.001 L 234.41854170811027 201.001 L 234.41854170811027 201.001 L 234.41854170811027 201.001 L 234.41854170811027 201.001 L 224.8504379649221 201.001 z" cy="190.95" cx="234.41854170811027" j="12" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5642" d="M 243.98664545129844 201.001 L 243.98664545129844 184.92100000000002 C 243.98664545129844 184.92100000000002 243.98664545129844 184.92100000000002 243.98664545129844 184.92100000000002 L 253.55474919448662 184.92100000000002 C 253.55474919448662 184.92100000000002 253.55474919448662 184.92100000000002 253.55474919448662 184.92100000000002 L 253.55474919448662 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 243.98664545129844 201.001 L 243.98664545129844 184.92100000000002 C 243.98664545129844 184.92100000000002 243.98664545129844 184.92100000000002 243.98664545129844 184.92100000000002 L 253.55474919448662 184.92100000000002 C 253.55474919448662 184.92100000000002 253.55474919448662 184.92100000000002 253.55474919448662 184.92100000000002 L 253.55474919448662 201.001 z " pathFrom="M 243.98664545129844 201.001 L 243.98664545129844 201.001 L 253.55474919448662 201.001 L 253.55474919448662 201.001 L 253.55474919448662 201.001 L 253.55474919448662 201.001 L 253.55474919448662 201.001 L 243.98664545129844 201.001 z" cy="184.92000000000002" cx="253.55474919448662" j="13" val="8" barHeight="16.08" barWidth="9.568103743188175"></path><path id="SvgjsPath5644" d="M 263.1228529376748 201.001 L 263.1228529376748 156.781 C 263.1228529376748 156.781 263.1228529376748 156.781 263.1228529376748 156.781 L 272.690956680863 156.781 C 272.690956680863 156.781 272.690956680863 156.781 272.690956680863 156.781 L 272.690956680863 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 263.1228529376748 201.001 L 263.1228529376748 156.781 C 263.1228529376748 156.781 263.1228529376748 156.781 263.1228529376748 156.781 L 272.690956680863 156.781 C 272.690956680863 156.781 272.690956680863 156.781 272.690956680863 156.781 L 272.690956680863 201.001 z " pathFrom="M 263.1228529376748 201.001 L 263.1228529376748 201.001 L 272.690956680863 201.001 L 272.690956680863 201.001 L 272.690956680863 201.001 L 272.690956680863 201.001 L 272.690956680863 201.001 L 263.1228529376748 201.001 z" cy="156.78" cx="272.690956680863" j="14" val="22" barHeight="44.22" barWidth="9.568103743188175"></path><path id="SvgjsPath5646" d="M 282.25906042405114 201.001 L 282.25906042405114 188.941 C 282.25906042405114 188.941 282.25906042405114 188.941 282.25906042405114 188.941 L 291.8271641672393 188.941 C 291.8271641672393 188.941 291.8271641672393 188.941 291.8271641672393 188.941 L 291.8271641672393 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 282.25906042405114 201.001 L 282.25906042405114 188.941 C 282.25906042405114 188.941 282.25906042405114 188.941 282.25906042405114 188.941 L 291.8271641672393 188.941 C 291.8271641672393 188.941 291.8271641672393 188.941 291.8271641672393 188.941 L 291.8271641672393 201.001 z " pathFrom="M 282.25906042405114 201.001 L 282.25906042405114 201.001 L 291.8271641672393 201.001 L 291.8271641672393 201.001 L 291.8271641672393 201.001 L 291.8271641672393 201.001 L 291.8271641672393 201.001 L 282.25906042405114 201.001 z" cy="188.94" cx="291.8271641672393" j="15" val="6" barHeight="12.06" barWidth="9.568103743188175"></path><path id="SvgjsPath5648" d="M 301.3952679104275 201.001 L 301.3952679104275 184.92100000000002 C 301.3952679104275 184.92100000000002 301.3952679104275 184.92100000000002 301.3952679104275 184.92100000000002 L 310.9633716536157 184.92100000000002 C 310.9633716536157 184.92100000000002 310.9633716536157 184.92100000000002 310.9633716536157 184.92100000000002 L 310.9633716536157 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 301.3952679104275 201.001 L 301.3952679104275 184.92100000000002 C 301.3952679104275 184.92100000000002 301.3952679104275 184.92100000000002 301.3952679104275 184.92100000000002 L 310.9633716536157 184.92100000000002 C 310.9633716536157 184.92100000000002 310.9633716536157 184.92100000000002 310.9633716536157 184.92100000000002 L 310.9633716536157 201.001 z " pathFrom="M 301.3952679104275 201.001 L 301.3952679104275 201.001 L 310.9633716536157 201.001 L 310.9633716536157 201.001 L 310.9633716536157 201.001 L 310.9633716536157 201.001 L 310.9633716536157 201.001 L 301.3952679104275 201.001 z" cy="184.92000000000002" cx="310.9633716536157" j="16" val="8" barHeight="16.08" barWidth="9.568103743188175"></path><path id="SvgjsPath5650" d="M 320.53147539680384 201.001 L 320.53147539680384 188.941 C 320.53147539680384 188.941 320.53147539680384 188.941 320.53147539680384 188.941 L 330.099579139992 188.941 C 330.099579139992 188.941 330.099579139992 188.941 330.099579139992 188.941 L 330.099579139992 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 320.53147539680384 201.001 L 320.53147539680384 188.941 C 320.53147539680384 188.941 320.53147539680384 188.941 320.53147539680384 188.941 L 330.099579139992 188.941 C 330.099579139992 188.941 330.099579139992 188.941 330.099579139992 188.941 L 330.099579139992 201.001 z " pathFrom="M 320.53147539680384 201.001 L 320.53147539680384 201.001 L 330.099579139992 201.001 L 330.099579139992 201.001 L 330.099579139992 201.001 L 330.099579139992 201.001 L 330.099579139992 201.001 L 320.53147539680384 201.001 z" cy="188.94" cx="330.099579139992" j="17" val="6" barHeight="12.06" barWidth="9.568103743188175"></path><path id="SvgjsPath5652" d="M 339.6676828831802 201.001 L 339.6676828831802 192.961 C 339.6676828831802 192.961 339.6676828831802 192.961 339.6676828831802 192.961 L 349.2357866263684 192.961 C 349.2357866263684 192.961 349.2357866263684 192.961 349.2357866263684 192.961 L 349.2357866263684 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 339.6676828831802 201.001 L 339.6676828831802 192.961 C 339.6676828831802 192.961 339.6676828831802 192.961 339.6676828831802 192.961 L 349.2357866263684 192.961 C 349.2357866263684 192.961 349.2357866263684 192.961 349.2357866263684 192.961 L 349.2357866263684 201.001 z " pathFrom="M 339.6676828831802 201.001 L 339.6676828831802 201.001 L 349.2357866263684 201.001 L 349.2357866263684 201.001 L 349.2357866263684 201.001 L 349.2357866263684 201.001 L 349.2357866263684 201.001 L 339.6676828831802 201.001 z" cy="192.96" cx="349.2357866263684" j="18" val="4" barHeight="8.04" barWidth="9.568103743188175"></path><path id="SvgjsPath5654" d="M 358.80389036955654 201.001 L 358.80389036955654 198.991 C 358.80389036955654 198.991 358.80389036955654 198.991 358.80389036955654 198.991 L 368.3719941127447 198.991 C 368.3719941127447 198.991 368.3719941127447 198.991 368.3719941127447 198.991 L 368.3719941127447 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 358.80389036955654 201.001 L 358.80389036955654 198.991 C 358.80389036955654 198.991 358.80389036955654 198.991 358.80389036955654 198.991 L 368.3719941127447 198.991 C 368.3719941127447 198.991 368.3719941127447 198.991 368.3719941127447 198.991 L 368.3719941127447 201.001 z " pathFrom="M 358.80389036955654 201.001 L 358.80389036955654 201.001 L 368.3719941127447 201.001 L 368.3719941127447 201.001 L 368.3719941127447 201.001 L 368.3719941127447 201.001 L 368.3719941127447 201.001 L 358.80389036955654 201.001 z" cy="198.99" cx="368.3719941127447" j="19" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5656" d="M 377.9400978559329 201.001 L 377.9400978559329 184.92100000000002 C 377.9400978559329 184.92100000000002 377.9400978559329 184.92100000000002 377.9400978559329 184.92100000000002 L 387.5082015991211 184.92100000000002 C 387.5082015991211 184.92100000000002 387.5082015991211 184.92100000000002 387.5082015991211 184.92100000000002 L 387.5082015991211 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 377.9400978559329 201.001 L 377.9400978559329 184.92100000000002 C 377.9400978559329 184.92100000000002 377.9400978559329 184.92100000000002 377.9400978559329 184.92100000000002 L 387.5082015991211 184.92100000000002 C 387.5082015991211 184.92100000000002 387.5082015991211 184.92100000000002 387.5082015991211 184.92100000000002 L 387.5082015991211 201.001 z " pathFrom="M 377.9400978559329 201.001 L 377.9400978559329 201.001 L 387.5082015991211 201.001 L 387.5082015991211 201.001 L 387.5082015991211 201.001 L 387.5082015991211 201.001 L 387.5082015991211 201.001 L 377.9400978559329 201.001 z" cy="184.92000000000002" cx="387.5082015991211" j="20" val="8" barHeight="16.08" barWidth="9.568103743188175"></path><path id="SvgjsPath5658" d="M 397.07630534230924 201.001 L 397.07630534230924 152.761 C 397.07630534230924 152.761 397.07630534230924 152.761 397.07630534230924 152.761 L 406.6444090854974 152.761 C 406.6444090854974 152.761 406.6444090854974 152.761 406.6444090854974 152.761 L 406.6444090854974 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 397.07630534230924 201.001 L 397.07630534230924 152.761 C 397.07630534230924 152.761 397.07630534230924 152.761 397.07630534230924 152.761 L 406.6444090854974 152.761 C 406.6444090854974 152.761 406.6444090854974 152.761 406.6444090854974 152.761 L 406.6444090854974 201.001 z " pathFrom="M 397.07630534230924 201.001 L 397.07630534230924 201.001 L 406.6444090854974 201.001 L 406.6444090854974 201.001 L 406.6444090854974 201.001 L 406.6444090854974 201.001 L 406.6444090854974 201.001 L 397.07630534230924 201.001 z" cy="152.76" cx="406.6444090854974" j="21" val="24" barHeight="48.24" barWidth="9.568103743188175"></path><path id="SvgjsPath5660" d="M 416.2125128286856 201.001 L 416.2125128286856 142.711 C 416.2125128286856 142.711 416.2125128286856 142.711 416.2125128286856 142.711 L 425.7806165718738 142.711 C 425.7806165718738 142.711 425.7806165718738 142.711 425.7806165718738 142.711 L 425.7806165718738 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 416.2125128286856 201.001 L 416.2125128286856 142.711 C 416.2125128286856 142.711 416.2125128286856 142.711 416.2125128286856 142.711 L 425.7806165718738 142.711 C 425.7806165718738 142.711 425.7806165718738 142.711 425.7806165718738 142.711 L 425.7806165718738 201.001 z " pathFrom="M 416.2125128286856 201.001 L 416.2125128286856 201.001 L 425.7806165718738 201.001 L 425.7806165718738 201.001 L 425.7806165718738 201.001 L 425.7806165718738 201.001 L 425.7806165718738 201.001 L 416.2125128286856 201.001 z" cy="142.71" cx="425.7806165718738" j="22" val="29" barHeight="58.29" barWidth="9.568103743188175"></path><path id="SvgjsPath5662" d="M 435.34872031506194 201.001 L 435.34872031506194 98.49100000000001 C 435.34872031506194 98.49100000000001 435.34872031506194 98.49100000000001 435.34872031506194 98.49100000000001 L 444.9168240582501 98.49100000000001 C 444.9168240582501 98.49100000000001 444.9168240582501 98.49100000000001 444.9168240582501 98.49100000000001 L 444.9168240582501 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 435.34872031506194 201.001 L 435.34872031506194 98.49100000000001 C 435.34872031506194 98.49100000000001 435.34872031506194 98.49100000000001 435.34872031506194 98.49100000000001 L 444.9168240582501 98.49100000000001 C 444.9168240582501 98.49100000000001 444.9168240582501 98.49100000000001 444.9168240582501 98.49100000000001 L 444.9168240582501 201.001 z " pathFrom="M 435.34872031506194 201.001 L 435.34872031506194 201.001 L 444.9168240582501 201.001 L 444.9168240582501 201.001 L 444.9168240582501 201.001 L 444.9168240582501 201.001 L 444.9168240582501 201.001 L 435.34872031506194 201.001 z" cy="98.49000000000001" cx="444.9168240582501" j="23" val="51" barHeight="102.50999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5664" d="M 454.4849278014383 201.001 L 454.4849278014383 120.60100000000001 C 454.4849278014383 120.60100000000001 454.4849278014383 120.60100000000001 454.4849278014383 120.60100000000001 L 464.0530315446265 120.60100000000001 C 464.0530315446265 120.60100000000001 464.0530315446265 120.60100000000001 464.0530315446265 120.60100000000001 L 464.0530315446265 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 454.4849278014383 201.001 L 454.4849278014383 120.60100000000001 C 454.4849278014383 120.60100000000001 454.4849278014383 120.60100000000001 454.4849278014383 120.60100000000001 L 464.0530315446265 120.60100000000001 C 464.0530315446265 120.60100000000001 464.0530315446265 120.60100000000001 464.0530315446265 120.60100000000001 L 464.0530315446265 201.001 z " pathFrom="M 454.4849278014383 201.001 L 454.4849278014383 201.001 L 464.0530315446265 201.001 L 464.0530315446265 201.001 L 464.0530315446265 201.001 L 464.0530315446265 201.001 L 464.0530315446265 201.001 L 454.4849278014383 201.001 z" cy="120.60000000000001" cx="464.0530315446265" j="24" val="40" barHeight="80.39999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5666" d="M 473.62113528781464 201.001 L 473.62113528781464 106.531 C 473.62113528781464 106.531 473.62113528781464 106.531 473.62113528781464 106.531 L 483.1892390310028 106.531 C 483.1892390310028 106.531 483.1892390310028 106.531 483.1892390310028 106.531 L 483.1892390310028 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 473.62113528781464 201.001 L 473.62113528781464 106.531 C 473.62113528781464 106.531 473.62113528781464 106.531 473.62113528781464 106.531 L 483.1892390310028 106.531 C 483.1892390310028 106.531 483.1892390310028 106.531 483.1892390310028 106.531 L 483.1892390310028 201.001 z " pathFrom="M 473.62113528781464 201.001 L 473.62113528781464 201.001 L 483.1892390310028 201.001 L 483.1892390310028 201.001 L 483.1892390310028 201.001 L 483.1892390310028 201.001 L 483.1892390310028 201.001 L 473.62113528781464 201.001 z" cy="106.53" cx="483.1892390310028" j="25" val="47" barHeight="94.47" barWidth="9.568103743188175"></path><path id="SvgjsPath5668" d="M 492.757342774191 201.001 L 492.757342774191 154.77100000000002 C 492.757342774191 154.77100000000002 492.757342774191 154.77100000000002 492.757342774191 154.77100000000002 L 502.3254465173792 154.77100000000002 C 502.3254465173792 154.77100000000002 502.3254465173792 154.77100000000002 502.3254465173792 154.77100000000002 L 502.3254465173792 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 492.757342774191 201.001 L 492.757342774191 154.77100000000002 C 492.757342774191 154.77100000000002 492.757342774191 154.77100000000002 492.757342774191 154.77100000000002 L 502.3254465173792 154.77100000000002 C 502.3254465173792 154.77100000000002 502.3254465173792 154.77100000000002 502.3254465173792 154.77100000000002 L 502.3254465173792 201.001 z " pathFrom="M 492.757342774191 201.001 L 492.757342774191 201.001 L 502.3254465173792 201.001 L 502.3254465173792 201.001 L 502.3254465173792 201.001 L 502.3254465173792 201.001 L 502.3254465173792 201.001 L 492.757342774191 201.001 z" cy="154.77" cx="502.3254465173792" j="26" val="23" barHeight="46.23" barWidth="9.568103743188175"></path><path id="SvgjsPath5670" d="M 511.8935502605673 201.001 L 511.8935502605673 148.741 C 511.8935502605673 148.741 511.8935502605673 148.741 511.8935502605673 148.741 L 521.4616540037555 148.741 C 521.4616540037555 148.741 521.4616540037555 148.741 521.4616540037555 148.741 L 521.4616540037555 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 511.8935502605673 201.001 L 511.8935502605673 148.741 C 511.8935502605673 148.741 511.8935502605673 148.741 511.8935502605673 148.741 L 521.4616540037555 148.741 C 521.4616540037555 148.741 521.4616540037555 148.741 521.4616540037555 148.741 L 521.4616540037555 201.001 z " pathFrom="M 511.8935502605673 201.001 L 511.8935502605673 201.001 L 521.4616540037555 201.001 L 521.4616540037555 201.001 L 521.4616540037555 201.001 L 521.4616540037555 201.001 L 521.4616540037555 201.001 L 511.8935502605673 201.001 z" cy="148.74" cx="521.4616540037555" j="27" val="26" barHeight="52.26" barWidth="9.568103743188175"></path><path id="SvgjsPath5672" d="M 531.0297577469437 201.001 L 531.0297577469437 100.501 C 531.0297577469437 100.501 531.0297577469437 100.501 531.0297577469437 100.501 L 540.5978614901319 100.501 C 540.5978614901319 100.501 540.5978614901319 100.501 540.5978614901319 100.501 L 540.5978614901319 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 531.0297577469437 201.001 L 531.0297577469437 100.501 C 531.0297577469437 100.501 531.0297577469437 100.501 531.0297577469437 100.501 L 540.5978614901319 100.501 C 540.5978614901319 100.501 540.5978614901319 100.501 540.5978614901319 100.501 L 540.5978614901319 201.001 z " pathFrom="M 531.0297577469437 201.001 L 531.0297577469437 201.001 L 540.5978614901319 201.001 L 540.5978614901319 201.001 L 540.5978614901319 201.001 L 540.5978614901319 201.001 L 540.5978614901319 201.001 L 531.0297577469437 201.001 z" cy="100.5" cx="540.5978614901319" j="28" val="50" barHeight="100.5" barWidth="9.568103743188175"></path><path id="SvgjsPath5674" d="M 550.16596523332 201.001 L 550.16596523332 148.741 C 550.16596523332 148.741 550.16596523332 148.741 550.16596523332 148.741 L 559.7340689765082 148.741 C 559.7340689765082 148.741 559.7340689765082 148.741 559.7340689765082 148.741 L 559.7340689765082 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 550.16596523332 201.001 L 550.16596523332 148.741 C 550.16596523332 148.741 550.16596523332 148.741 550.16596523332 148.741 L 559.7340689765082 148.741 C 559.7340689765082 148.741 559.7340689765082 148.741 559.7340689765082 148.741 L 559.7340689765082 201.001 z " pathFrom="M 550.16596523332 201.001 L 550.16596523332 201.001 L 559.7340689765082 201.001 L 559.7340689765082 201.001 L 559.7340689765082 201.001 L 559.7340689765082 201.001 L 559.7340689765082 201.001 L 550.16596523332 201.001 z" cy="148.74" cx="559.7340689765082" j="29" val="26" barHeight="52.26" barWidth="9.568103743188175"></path><path id="SvgjsPath5676" d="M 569.3021727196964 201.001 L 569.3021727196964 118.59100000000001 C 569.3021727196964 118.59100000000001 569.3021727196964 118.59100000000001 569.3021727196964 118.59100000000001 L 578.8702764628846 118.59100000000001 C 578.8702764628846 118.59100000000001 578.8702764628846 118.59100000000001 578.8702764628846 118.59100000000001 L 578.8702764628846 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 569.3021727196964 201.001 L 569.3021727196964 118.59100000000001 C 569.3021727196964 118.59100000000001 569.3021727196964 118.59100000000001 569.3021727196964 118.59100000000001 L 578.8702764628846 118.59100000000001 C 578.8702764628846 118.59100000000001 578.8702764628846 118.59100000000001 578.8702764628846 118.59100000000001 L 578.8702764628846 201.001 z " pathFrom="M 569.3021727196964 201.001 L 569.3021727196964 201.001 L 578.8702764628846 201.001 L 578.8702764628846 201.001 L 578.8702764628846 201.001 L 578.8702764628846 201.001 L 578.8702764628846 201.001 L 569.3021727196964 201.001 z" cy="118.59" cx="578.8702764628846" j="30" val="41" barHeight="82.41" barWidth="9.568103743188175"></path><path id="SvgjsPath5678" d="M 588.4383802060727 201.001 L 588.4383802060727 156.781 C 588.4383802060727 156.781 588.4383802060727 156.781 588.4383802060727 156.781 L 598.0064839492609 156.781 C 598.0064839492609 156.781 598.0064839492609 156.781 598.0064839492609 156.781 L 598.0064839492609 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 588.4383802060727 201.001 L 588.4383802060727 156.781 C 588.4383802060727 156.781 588.4383802060727 156.781 588.4383802060727 156.781 L 598.0064839492609 156.781 C 598.0064839492609 156.781 598.0064839492609 156.781 598.0064839492609 156.781 L 598.0064839492609 201.001 z " pathFrom="M 588.4383802060727 201.001 L 588.4383802060727 201.001 L 598.0064839492609 201.001 L 598.0064839492609 201.001 L 598.0064839492609 201.001 L 598.0064839492609 201.001 L 598.0064839492609 201.001 L 588.4383802060727 201.001 z" cy="156.78" cx="598.0064839492609" j="31" val="22" barHeight="44.22" barWidth="9.568103743188175"></path><path id="SvgjsPath5680" d="M 607.5745876924491 201.001 L 607.5745876924491 108.54100000000001 C 607.5745876924491 108.54100000000001 607.5745876924491 108.54100000000001 607.5745876924491 108.54100000000001 L 617.1426914356373 108.54100000000001 C 617.1426914356373 108.54100000000001 617.1426914356373 108.54100000000001 617.1426914356373 108.54100000000001 L 617.1426914356373 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 607.5745876924491 201.001 L 607.5745876924491 108.54100000000001 C 607.5745876924491 108.54100000000001 607.5745876924491 108.54100000000001 607.5745876924491 108.54100000000001 L 617.1426914356373 108.54100000000001 C 617.1426914356373 108.54100000000001 617.1426914356373 108.54100000000001 617.1426914356373 108.54100000000001 L 617.1426914356373 201.001 z " pathFrom="M 607.5745876924491 201.001 L 607.5745876924491 201.001 L 617.1426914356373 201.001 L 617.1426914356373 201.001 L 617.1426914356373 201.001 L 617.1426914356373 201.001 L 617.1426914356373 201.001 L 607.5745876924491 201.001 z" cy="108.54" cx="617.1426914356373" j="32" val="46" barHeight="92.46" barWidth="9.568103743188175"></path><path id="SvgjsPath5682" d="M 626.7107951788254 201.001 L 626.7107951788254 106.531 C 626.7107951788254 106.531 626.7107951788254 106.531 626.7107951788254 106.531 L 636.2788989220136 106.531 C 636.2788989220136 106.531 636.2788989220136 106.531 636.2788989220136 106.531 L 636.2788989220136 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 626.7107951788254 201.001 L 626.7107951788254 106.531 C 626.7107951788254 106.531 626.7107951788254 106.531 626.7107951788254 106.531 L 636.2788989220136 106.531 C 636.2788989220136 106.531 636.2788989220136 106.531 636.2788989220136 106.531 L 636.2788989220136 201.001 z " pathFrom="M 626.7107951788254 201.001 L 626.7107951788254 201.001 L 636.2788989220136 201.001 L 636.2788989220136 201.001 L 636.2788989220136 201.001 L 636.2788989220136 201.001 L 636.2788989220136 201.001 L 626.7107951788254 201.001 z" cy="106.53" cx="636.2788989220136" j="33" val="47" barHeight="94.47" barWidth="9.568103743188175"></path><path id="SvgjsPath5684" d="M 645.8470026652018 201.001 L 645.8470026652018 38.190999999999995 C 645.8470026652018 38.190999999999995 645.8470026652018 38.190999999999995 645.8470026652018 38.190999999999995 L 655.41510640839 38.190999999999995 C 655.41510640839 38.190999999999995 655.41510640839 38.190999999999995 655.41510640839 38.190999999999995 L 655.41510640839 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 645.8470026652018 201.001 L 645.8470026652018 38.190999999999995 C 645.8470026652018 38.190999999999995 645.8470026652018 38.190999999999995 645.8470026652018 38.190999999999995 L 655.41510640839 38.190999999999995 C 655.41510640839 38.190999999999995 655.41510640839 38.190999999999995 655.41510640839 38.190999999999995 L 655.41510640839 201.001 z " pathFrom="M 645.8470026652018 201.001 L 645.8470026652018 201.001 L 655.41510640839 201.001 L 655.41510640839 201.001 L 655.41510640839 201.001 L 655.41510640839 201.001 L 655.41510640839 201.001 L 645.8470026652018 201.001 z" cy="38.19" cx="655.41510640839" j="34" val="81" barHeight="162.81" barWidth="9.568103743188175"></path><path id="SvgjsPath5686" d="M 664.9832101515781 201.001 L 664.9832101515781 108.54100000000001 C 664.9832101515781 108.54100000000001 664.9832101515781 108.54100000000001 664.9832101515781 108.54100000000001 L 674.5513138947663 108.54100000000001 C 674.5513138947663 108.54100000000001 674.5513138947663 108.54100000000001 674.5513138947663 108.54100000000001 L 674.5513138947663 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 664.9832101515781 201.001 L 664.9832101515781 108.54100000000001 C 664.9832101515781 108.54100000000001 664.9832101515781 108.54100000000001 664.9832101515781 108.54100000000001 L 674.5513138947663 108.54100000000001 C 674.5513138947663 108.54100000000001 674.5513138947663 108.54100000000001 674.5513138947663 108.54100000000001 L 674.5513138947663 201.001 z " pathFrom="M 664.9832101515781 201.001 L 664.9832101515781 201.001 L 674.5513138947663 201.001 L 674.5513138947663 201.001 L 674.5513138947663 201.001 L 674.5513138947663 201.001 L 674.5513138947663 201.001 L 664.9832101515781 201.001 z" cy="108.54" cx="674.5513138947663" j="35" val="46" barHeight="92.46" barWidth="9.568103743188175"></path><path id="SvgjsPath5688" d="M 684.1194176379545 201.001 L 684.1194176379545 188.941 C 684.1194176379545 188.941 684.1194176379545 188.941 684.1194176379545 188.941 L 693.6875213811427 188.941 C 693.6875213811427 188.941 693.6875213811427 188.941 693.6875213811427 188.941 L 693.6875213811427 201.001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="0" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 684.1194176379545 201.001 L 684.1194176379545 188.941 C 684.1194176379545 188.941 684.1194176379545 188.941 684.1194176379545 188.941 L 693.6875213811427 188.941 C 693.6875213811427 188.941 693.6875213811427 188.941 693.6875213811427 188.941 L 693.6875213811427 201.001 z " pathFrom="M 684.1194176379545 201.001 L 684.1194176379545 201.001 L 693.6875213811427 201.001 L 693.6875213811427 201.001 L 693.6875213811427 201.001 L 693.6875213811427 201.001 L 693.6875213811427 201.001 L 684.1194176379545 201.001 z" cy="188.94" cx="693.6875213811427" j="36" val="6" barHeight="12.06" barWidth="9.568103743188175"></path><g id="SvgjsG5614" class="apexcharts-bar-goals-markers"><g id="SvgjsG5615" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5617" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5619" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5621" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5623" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5625" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5627" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5629" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5631" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5633" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5635" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5637" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5639" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5641" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5643" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5645" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5647" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5649" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5651" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5653" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5655" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5657" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5659" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5661" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5663" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5665" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5667" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5669" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5671" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5673" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5675" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5677" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5679" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5681" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5683" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5685" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5687" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g></g></g><g id="SvgjsG5689" class="apexcharts-series" seriesName="Social" rel="2" data:realIndex="1"><path id="SvgjsPath5693" d="M -4.784051871594087 198.99200000000002 L -4.784051871594087 194.972 C -4.784051871594087 194.972 -4.784051871594087 194.972 -4.784051871594087 194.972 L 4.784051871594087 194.972 C 4.784051871594087 194.972 4.784051871594087 194.972 4.784051871594087 194.972 L 4.784051871594087 198.99200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M -4.784051871594087 198.99200000000002 L -4.784051871594087 194.972 C -4.784051871594087 194.972 -4.784051871594087 194.972 -4.784051871594087 194.972 L 4.784051871594087 194.972 C 4.784051871594087 194.972 4.784051871594087 194.972 4.784051871594087 194.972 L 4.784051871594087 198.99200000000002 z " pathFrom="M -4.784051871594087 198.99200000000002 L -4.784051871594087 198.99200000000002 L 4.784051871594087 198.99200000000002 L 4.784051871594087 198.99200000000002 L 4.784051871594087 198.99200000000002 L 4.784051871594087 198.99200000000002 L 4.784051871594087 198.99200000000002 L -4.784051871594087 198.99200000000002 z" cy="194.971" cx="4.784051871594087" j="0" val="2" barHeight="4.02" barWidth="9.568103743188175"></path><path id="SvgjsPath5695" d="M 14.352155614782262 201.002 L 14.352155614782262 190.952 C 14.352155614782262 190.952 14.352155614782262 190.952 14.352155614782262 190.952 L 23.920259357970437 190.952 C 23.920259357970437 190.952 23.920259357970437 190.952 23.920259357970437 190.952 L 23.920259357970437 201.002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 14.352155614782262 201.002 L 14.352155614782262 190.952 C 14.352155614782262 190.952 14.352155614782262 190.952 14.352155614782262 190.952 L 23.920259357970437 190.952 C 23.920259357970437 190.952 23.920259357970437 190.952 23.920259357970437 190.952 L 23.920259357970437 201.002 z " pathFrom="M 14.352155614782262 201.002 L 14.352155614782262 201.002 L 23.920259357970437 201.002 L 23.920259357970437 201.002 L 23.920259357970437 201.002 L 23.920259357970437 201.002 L 23.920259357970437 201.002 L 14.352155614782262 201.002 z" cy="190.951" cx="23.920259357970437" j="1" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5697" d="M 33.48836310115861 201.002 L 33.48836310115861 192.96200000000002 C 33.48836310115861 192.96200000000002 33.48836310115861 192.96200000000002 33.48836310115861 192.96200000000002 L 43.05646684434679 192.96200000000002 C 43.05646684434679 192.96200000000002 43.05646684434679 192.96200000000002 43.05646684434679 192.96200000000002 L 43.05646684434679 201.002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 33.48836310115861 201.002 L 33.48836310115861 192.96200000000002 C 33.48836310115861 192.96200000000002 33.48836310115861 192.96200000000002 33.48836310115861 192.96200000000002 L 43.05646684434679 192.96200000000002 C 43.05646684434679 192.96200000000002 43.05646684434679 192.96200000000002 43.05646684434679 192.96200000000002 L 43.05646684434679 201.002 z " pathFrom="M 33.48836310115861 201.002 L 33.48836310115861 201.002 L 43.05646684434679 201.002 L 43.05646684434679 201.002 L 43.05646684434679 201.002 L 43.05646684434679 201.002 L 43.05646684434679 201.002 L 33.48836310115861 201.002 z" cy="192.961" cx="43.05646684434679" j="2" val="4" barHeight="8.04" barWidth="9.568103743188175"></path><path id="SvgjsPath5699" d="M 52.62457058753496 201.002 L 52.62457058753496 194.972 C 52.62457058753496 194.972 52.62457058753496 194.972 52.62457058753496 194.972 L 62.192674330723136 194.972 C 62.192674330723136 194.972 62.192674330723136 194.972 62.192674330723136 194.972 L 62.192674330723136 201.002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 52.62457058753496 201.002 L 52.62457058753496 194.972 C 52.62457058753496 194.972 52.62457058753496 194.972 52.62457058753496 194.972 L 62.192674330723136 194.972 C 62.192674330723136 194.972 62.192674330723136 194.972 62.192674330723136 194.972 L 62.192674330723136 201.002 z " pathFrom="M 52.62457058753496 201.002 L 52.62457058753496 201.002 L 62.192674330723136 201.002 L 62.192674330723136 201.002 L 62.192674330723136 201.002 L 62.192674330723136 201.002 L 62.192674330723136 201.002 L 52.62457058753496 201.002 z" cy="194.971" cx="62.192674330723136" j="3" val="3" barHeight="6.03" barWidth="9.568103743188175"></path><path id="SvgjsPath5701" d="M 71.76077807391131 201.002 L 71.76077807391131 194.972 C 71.76077807391131 194.972 71.76077807391131 194.972 71.76077807391131 194.972 L 81.32888181709949 194.972 C 81.32888181709949 194.972 81.32888181709949 194.972 81.32888181709949 194.972 L 81.32888181709949 201.002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 71.76077807391131 201.002 L 71.76077807391131 194.972 C 71.76077807391131 194.972 71.76077807391131 194.972 71.76077807391131 194.972 L 81.32888181709949 194.972 C 81.32888181709949 194.972 81.32888181709949 194.972 81.32888181709949 194.972 L 81.32888181709949 201.002 z " pathFrom="M 71.76077807391131 201.002 L 71.76077807391131 201.002 L 81.32888181709949 201.002 L 81.32888181709949 201.002 L 81.32888181709949 201.002 L 81.32888181709949 201.002 L 81.32888181709949 201.002 L 71.76077807391131 201.002 z" cy="194.971" cx="81.32888181709949" j="4" val="3" barHeight="6.03" barWidth="9.568103743188175"></path><path id="SvgjsPath5703" d="M 90.89698556028766 198.99200000000002 L 90.89698556028766 196.98200000000003 C 90.89698556028766 196.98200000000003 90.89698556028766 196.98200000000003 90.89698556028766 196.98200000000003 L 100.46508930347584 196.98200000000003 C 100.46508930347584 196.98200000000003 100.46508930347584 196.98200000000003 100.46508930347584 196.98200000000003 L 100.46508930347584 198.99200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 90.89698556028766 198.99200000000002 L 90.89698556028766 196.98200000000003 C 90.89698556028766 196.98200000000003 90.89698556028766 196.98200000000003 90.89698556028766 196.98200000000003 L 100.46508930347584 196.98200000000003 C 100.46508930347584 196.98200000000003 100.46508930347584 196.98200000000003 100.46508930347584 196.98200000000003 L 100.46508930347584 198.99200000000002 z " pathFrom="M 90.89698556028766 198.99200000000002 L 90.89698556028766 198.99200000000002 L 100.46508930347584 198.99200000000002 L 100.46508930347584 198.99200000000002 L 100.46508930347584 198.99200000000002 L 100.46508930347584 198.99200000000002 L 100.46508930347584 198.99200000000002 L 90.89698556028766 198.99200000000002 z" cy="196.98100000000002" cx="100.46508930347584" j="5" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5705" d="M 110.03319304666401 198.99200000000002 L 110.03319304666401 190.95200000000003 C 110.03319304666401 190.95200000000003 110.03319304666401 190.95200000000003 110.03319304666401 190.95200000000003 L 119.60129678985219 190.95200000000003 C 119.60129678985219 190.95200000000003 119.60129678985219 190.95200000000003 119.60129678985219 190.95200000000003 L 119.60129678985219 198.99200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 110.03319304666401 198.99200000000002 L 110.03319304666401 190.95200000000003 C 110.03319304666401 190.95200000000003 110.03319304666401 190.95200000000003 110.03319304666401 190.95200000000003 L 119.60129678985219 190.95200000000003 C 119.60129678985219 190.95200000000003 119.60129678985219 190.95200000000003 119.60129678985219 190.95200000000003 L 119.60129678985219 198.99200000000002 z " pathFrom="M 110.03319304666401 198.99200000000002 L 110.03319304666401 198.99200000000002 L 119.60129678985219 198.99200000000002 L 119.60129678985219 198.99200000000002 L 119.60129678985219 198.99200000000002 L 119.60129678985219 198.99200000000002 L 119.60129678985219 198.99200000000002 L 110.03319304666401 198.99200000000002 z" cy="190.95100000000002" cx="119.60129678985219" j="6" val="4" barHeight="8.04" barWidth="9.568103743188175"></path><path id="SvgjsPath5707" d="M 129.16940053304035 201.002 L 129.16940053304035 186.93200000000002 C 129.16940053304035 186.93200000000002 129.16940053304035 186.93200000000002 129.16940053304035 186.93200000000002 L 138.73750427622852 186.93200000000002 C 138.73750427622852 186.93200000000002 138.73750427622852 186.93200000000002 138.73750427622852 186.93200000000002 L 138.73750427622852 201.002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 129.16940053304035 201.002 L 129.16940053304035 186.93200000000002 C 129.16940053304035 186.93200000000002 129.16940053304035 186.93200000000002 129.16940053304035 186.93200000000002 L 138.73750427622852 186.93200000000002 C 138.73750427622852 186.93200000000002 138.73750427622852 186.93200000000002 138.73750427622852 186.93200000000002 L 138.73750427622852 201.002 z " pathFrom="M 129.16940053304035 201.002 L 129.16940053304035 201.002 L 138.73750427622852 201.002 L 138.73750427622852 201.002 L 138.73750427622852 201.002 L 138.73750427622852 201.002 L 138.73750427622852 201.002 L 129.16940053304035 201.002 z" cy="186.931" cx="138.73750427622852" j="7" val="7" barHeight="14.07" barWidth="9.568103743188175"></path><path id="SvgjsPath5709" d="M 148.3056080194167 201.002 L 148.3056080194167 190.952 C 148.3056080194167 190.952 148.3056080194167 190.952 148.3056080194167 190.952 L 157.87371176260487 190.952 C 157.87371176260487 190.952 157.87371176260487 190.952 157.87371176260487 190.952 L 157.87371176260487 201.002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 148.3056080194167 201.002 L 148.3056080194167 190.952 C 148.3056080194167 190.952 148.3056080194167 190.952 148.3056080194167 190.952 L 157.87371176260487 190.952 C 157.87371176260487 190.952 157.87371176260487 190.952 157.87371176260487 190.952 L 157.87371176260487 201.002 z " pathFrom="M 148.3056080194167 201.002 L 148.3056080194167 201.002 L 157.87371176260487 201.002 L 157.87371176260487 201.002 L 157.87371176260487 201.002 L 157.87371176260487 201.002 L 157.87371176260487 201.002 L 148.3056080194167 201.002 z" cy="190.951" cx="157.87371176260487" j="8" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5711" d="M 167.44181550579304 201.002 L 167.44181550579304 198.99200000000002 C 167.44181550579304 198.99200000000002 167.44181550579304 198.99200000000002 167.44181550579304 198.99200000000002 L 177.00991924898122 198.99200000000002 C 177.00991924898122 198.99200000000002 177.00991924898122 198.99200000000002 177.00991924898122 198.99200000000002 L 177.00991924898122 201.002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 167.44181550579304 201.002 L 167.44181550579304 198.99200000000002 C 167.44181550579304 198.99200000000002 167.44181550579304 198.99200000000002 167.44181550579304 198.99200000000002 L 177.00991924898122 198.99200000000002 C 177.00991924898122 198.99200000000002 177.00991924898122 198.99200000000002 177.00991924898122 198.99200000000002 L 177.00991924898122 201.002 z " pathFrom="M 167.44181550579304 201.002 L 167.44181550579304 201.002 L 177.00991924898122 201.002 L 177.00991924898122 201.002 L 177.00991924898122 201.002 L 177.00991924898122 201.002 L 177.00991924898122 201.002 L 167.44181550579304 201.002 z" cy="198.991" cx="177.00991924898122" j="9" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5713" d="M 186.5780229921694 196.982 L 186.5780229921694 192.962 C 186.5780229921694 192.962 186.5780229921694 192.962 186.5780229921694 192.962 L 196.14612673535757 192.962 C 196.14612673535757 192.962 196.14612673535757 192.962 196.14612673535757 192.962 L 196.14612673535757 196.982 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 186.5780229921694 196.982 L 186.5780229921694 192.962 C 186.5780229921694 192.962 186.5780229921694 192.962 186.5780229921694 192.962 L 196.14612673535757 192.962 C 196.14612673535757 192.962 196.14612673535757 192.962 196.14612673535757 192.962 L 196.14612673535757 196.982 z " pathFrom="M 186.5780229921694 196.982 L 186.5780229921694 196.982 L 196.14612673535757 196.982 L 196.14612673535757 196.982 L 196.14612673535757 196.982 L 196.14612673535757 196.982 L 196.14612673535757 196.982 L 186.5780229921694 196.982 z" cy="192.96099999999998" cx="196.14612673535757" j="10" val="2" barHeight="4.02" barWidth="9.568103743188175"></path><path id="SvgjsPath5715" d="M 205.71423047854574 176.882 L 205.71423047854574 166.832 C 205.71423047854574 166.832 205.71423047854574 166.832 205.71423047854574 166.832 L 215.28233422173392 166.832 C 215.28233422173392 166.832 215.28233422173392 166.832 215.28233422173392 166.832 L 215.28233422173392 176.882 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 205.71423047854574 176.882 L 205.71423047854574 166.832 C 205.71423047854574 166.832 205.71423047854574 166.832 205.71423047854574 166.832 L 215.28233422173392 166.832 C 215.28233422173392 166.832 215.28233422173392 166.832 215.28233422173392 166.832 L 215.28233422173392 176.882 z " pathFrom="M 205.71423047854574 176.882 L 205.71423047854574 176.882 L 215.28233422173392 176.882 L 215.28233422173392 176.882 L 215.28233422173392 176.882 L 215.28233422173392 176.882 L 215.28233422173392 176.882 L 205.71423047854574 176.882 z" cy="166.831" cx="215.28233422173392" j="11" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5717" d="M 224.8504379649221 190.952 L 224.8504379649221 184.922 C 224.8504379649221 184.922 224.8504379649221 184.922 224.8504379649221 184.922 L 234.41854170811027 184.922 C 234.41854170811027 184.922 234.41854170811027 184.922 234.41854170811027 184.922 L 234.41854170811027 190.952 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 224.8504379649221 190.952 L 224.8504379649221 184.922 C 224.8504379649221 184.922 224.8504379649221 184.922 224.8504379649221 184.922 L 234.41854170811027 184.922 C 234.41854170811027 184.922 234.41854170811027 184.922 234.41854170811027 184.922 L 234.41854170811027 190.952 z " pathFrom="M 224.8504379649221 190.952 L 224.8504379649221 190.952 L 234.41854170811027 190.952 L 234.41854170811027 190.952 L 234.41854170811027 190.952 L 234.41854170811027 190.952 L 234.41854170811027 190.952 L 224.8504379649221 190.952 z" cy="184.921" cx="234.41854170811027" j="12" val="3" barHeight="6.03" barWidth="9.568103743188175"></path><path id="SvgjsPath5719" d="M 243.98664545129844 184.92200000000003 L 243.98664545129844 180.90200000000002 C 243.98664545129844 180.90200000000002 243.98664545129844 180.90200000000002 243.98664545129844 180.90200000000002 L 253.55474919448662 180.90200000000002 C 253.55474919448662 180.90200000000002 253.55474919448662 180.90200000000002 253.55474919448662 180.90200000000002 L 253.55474919448662 184.92200000000003 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 243.98664545129844 184.92200000000003 L 243.98664545129844 180.90200000000002 C 243.98664545129844 180.90200000000002 243.98664545129844 180.90200000000002 243.98664545129844 180.90200000000002 L 253.55474919448662 180.90200000000002 C 253.55474919448662 180.90200000000002 253.55474919448662 180.90200000000002 253.55474919448662 180.90200000000002 L 253.55474919448662 184.92200000000003 z " pathFrom="M 243.98664545129844 184.92200000000003 L 243.98664545129844 184.92200000000003 L 253.55474919448662 184.92200000000003 L 253.55474919448662 184.92200000000003 L 253.55474919448662 184.92200000000003 L 253.55474919448662 184.92200000000003 L 253.55474919448662 184.92200000000003 L 243.98664545129844 184.92200000000003 z" cy="180.901" cx="253.55474919448662" j="13" val="2" barHeight="4.02" barWidth="9.568103743188175"></path><path id="SvgjsPath5721" d="M 263.1228529376748 156.782 L 263.1228529376748 144.722 C 263.1228529376748 144.722 263.1228529376748 144.722 263.1228529376748 144.722 L 272.690956680863 144.722 C 272.690956680863 144.722 272.690956680863 144.722 272.690956680863 144.722 L 272.690956680863 156.782 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 263.1228529376748 156.782 L 263.1228529376748 144.722 C 263.1228529376748 144.722 263.1228529376748 144.722 263.1228529376748 144.722 L 272.690956680863 144.722 C 272.690956680863 144.722 272.690956680863 144.722 272.690956680863 144.722 L 272.690956680863 156.782 z " pathFrom="M 263.1228529376748 156.782 L 263.1228529376748 156.782 L 272.690956680863 156.782 L 272.690956680863 156.782 L 272.690956680863 156.782 L 272.690956680863 156.782 L 272.690956680863 156.782 L 263.1228529376748 156.782 z" cy="144.721" cx="272.690956680863" j="14" val="6" barHeight="12.06" barWidth="9.568103743188175"></path><path id="SvgjsPath5723" d="M 282.25906042405114 188.942 L 282.25906042405114 174.872 C 282.25906042405114 174.872 282.25906042405114 174.872 282.25906042405114 174.872 L 291.8271641672393 174.872 C 291.8271641672393 174.872 291.8271641672393 174.872 291.8271641672393 174.872 L 291.8271641672393 188.942 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 282.25906042405114 188.942 L 282.25906042405114 174.872 C 282.25906042405114 174.872 282.25906042405114 174.872 282.25906042405114 174.872 L 291.8271641672393 174.872 C 291.8271641672393 174.872 291.8271641672393 174.872 291.8271641672393 174.872 L 291.8271641672393 188.942 z " pathFrom="M 282.25906042405114 188.942 L 282.25906042405114 188.942 L 291.8271641672393 188.942 L 291.8271641672393 188.942 L 291.8271641672393 188.942 L 291.8271641672393 188.942 L 291.8271641672393 188.942 L 282.25906042405114 188.942 z" cy="174.871" cx="291.8271641672393" j="15" val="7" barHeight="14.07" barWidth="9.568103743188175"></path><path id="SvgjsPath5725" d="M 301.3952679104275 184.92200000000003 L 301.3952679104275 170.85200000000003 C 301.3952679104275 170.85200000000003 301.3952679104275 170.85200000000003 301.3952679104275 170.85200000000003 L 310.9633716536157 170.85200000000003 C 310.9633716536157 170.85200000000003 310.9633716536157 170.85200000000003 310.9633716536157 170.85200000000003 L 310.9633716536157 184.92200000000003 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 301.3952679104275 184.92200000000003 L 301.3952679104275 170.85200000000003 C 301.3952679104275 170.85200000000003 301.3952679104275 170.85200000000003 301.3952679104275 170.85200000000003 L 310.9633716536157 170.85200000000003 C 310.9633716536157 170.85200000000003 310.9633716536157 170.85200000000003 310.9633716536157 170.85200000000003 L 310.9633716536157 184.92200000000003 z " pathFrom="M 301.3952679104275 184.92200000000003 L 301.3952679104275 184.92200000000003 L 310.9633716536157 184.92200000000003 L 310.9633716536157 184.92200000000003 L 310.9633716536157 184.92200000000003 L 310.9633716536157 184.92200000000003 L 310.9633716536157 184.92200000000003 L 301.3952679104275 184.92200000000003 z" cy="170.85100000000003" cx="310.9633716536157" j="16" val="7" barHeight="14.07" barWidth="9.568103743188175"></path><path id="SvgjsPath5727" d="M 320.53147539680384 188.942 L 320.53147539680384 186.93200000000002 C 320.53147539680384 186.93200000000002 320.53147539680384 186.93200000000002 320.53147539680384 186.93200000000002 L 330.099579139992 186.93200000000002 C 330.099579139992 186.93200000000002 330.099579139992 186.93200000000002 330.099579139992 186.93200000000002 L 330.099579139992 188.942 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 320.53147539680384 188.942 L 320.53147539680384 186.93200000000002 C 320.53147539680384 186.93200000000002 320.53147539680384 186.93200000000002 320.53147539680384 186.93200000000002 L 330.099579139992 186.93200000000002 C 330.099579139992 186.93200000000002 330.099579139992 186.93200000000002 330.099579139992 186.93200000000002 L 330.099579139992 188.942 z " pathFrom="M 320.53147539680384 188.942 L 320.53147539680384 188.942 L 330.099579139992 188.942 L 330.099579139992 188.942 L 330.099579139992 188.942 L 330.099579139992 188.942 L 330.099579139992 188.942 L 320.53147539680384 188.942 z" cy="186.931" cx="330.099579139992" j="17" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5729" d="M 339.6676828831802 192.96200000000002 L 339.6676828831802 182.912 C 339.6676828831802 182.912 339.6676828831802 182.912 339.6676828831802 182.912 L 349.2357866263684 182.912 C 349.2357866263684 182.912 349.2357866263684 182.912 349.2357866263684 182.912 L 349.2357866263684 192.96200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 339.6676828831802 192.96200000000002 L 339.6676828831802 182.912 C 339.6676828831802 182.912 339.6676828831802 182.912 339.6676828831802 182.912 L 349.2357866263684 182.912 C 349.2357866263684 182.912 349.2357866263684 182.912 349.2357866263684 182.912 L 349.2357866263684 192.96200000000002 z " pathFrom="M 339.6676828831802 192.96200000000002 L 339.6676828831802 192.96200000000002 L 349.2357866263684 192.96200000000002 L 349.2357866263684 192.96200000000002 L 349.2357866263684 192.96200000000002 L 349.2357866263684 192.96200000000002 L 349.2357866263684 192.96200000000002 L 339.6676828831802 192.96200000000002 z" cy="182.911" cx="349.2357866263684" j="18" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5731" d="M 358.80389036955654 198.99200000000002 L 358.80389036955654 188.942 C 358.80389036955654 188.942 358.80389036955654 188.942 358.80389036955654 188.942 L 368.3719941127447 188.942 C 368.3719941127447 188.942 368.3719941127447 188.942 368.3719941127447 188.942 L 368.3719941127447 198.99200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 358.80389036955654 198.99200000000002 L 358.80389036955654 188.942 C 358.80389036955654 188.942 358.80389036955654 188.942 358.80389036955654 188.942 L 368.3719941127447 188.942 C 368.3719941127447 188.942 368.3719941127447 188.942 368.3719941127447 188.942 L 368.3719941127447 198.99200000000002 z " pathFrom="M 358.80389036955654 198.99200000000002 L 358.80389036955654 198.99200000000002 L 368.3719941127447 198.99200000000002 L 368.3719941127447 198.99200000000002 L 368.3719941127447 198.99200000000002 L 368.3719941127447 198.99200000000002 L 368.3719941127447 198.99200000000002 L 358.80389036955654 198.99200000000002 z" cy="188.941" cx="368.3719941127447" j="19" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5733" d="M 377.9400978559329 184.92200000000003 L 377.9400978559329 180.90200000000002 C 377.9400978559329 180.90200000000002 377.9400978559329 180.90200000000002 377.9400978559329 180.90200000000002 L 387.5082015991211 180.90200000000002 C 387.5082015991211 180.90200000000002 387.5082015991211 180.90200000000002 387.5082015991211 180.90200000000002 L 387.5082015991211 184.92200000000003 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 377.9400978559329 184.92200000000003 L 377.9400978559329 180.90200000000002 C 377.9400978559329 180.90200000000002 377.9400978559329 180.90200000000002 377.9400978559329 180.90200000000002 L 387.5082015991211 180.90200000000002 C 387.5082015991211 180.90200000000002 387.5082015991211 180.90200000000002 387.5082015991211 180.90200000000002 L 387.5082015991211 184.92200000000003 z " pathFrom="M 377.9400978559329 184.92200000000003 L 377.9400978559329 184.92200000000003 L 387.5082015991211 184.92200000000003 L 387.5082015991211 184.92200000000003 L 387.5082015991211 184.92200000000003 L 387.5082015991211 184.92200000000003 L 387.5082015991211 184.92200000000003 L 377.9400978559329 184.92200000000003 z" cy="180.901" cx="387.5082015991211" j="20" val="2" barHeight="4.02" barWidth="9.568103743188175"></path><path id="SvgjsPath5735" d="M 397.07630534230924 152.762 L 397.07630534230924 128.642 C 397.07630534230924 128.642 397.07630534230924 128.642 397.07630534230924 128.642 L 406.6444090854974 128.642 C 406.6444090854974 128.642 406.6444090854974 128.642 406.6444090854974 128.642 L 406.6444090854974 152.762 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 397.07630534230924 152.762 L 397.07630534230924 128.642 C 397.07630534230924 128.642 397.07630534230924 128.642 397.07630534230924 128.642 L 406.6444090854974 128.642 C 406.6444090854974 128.642 406.6444090854974 128.642 406.6444090854974 128.642 L 406.6444090854974 152.762 z " pathFrom="M 397.07630534230924 152.762 L 397.07630534230924 152.762 L 406.6444090854974 152.762 L 406.6444090854974 152.762 L 406.6444090854974 152.762 L 406.6444090854974 152.762 L 406.6444090854974 152.762 L 397.07630534230924 152.762 z" cy="128.641" cx="406.6444090854974" j="21" val="12" barHeight="24.12" barWidth="9.568103743188175"></path><path id="SvgjsPath5737" d="M 416.2125128286856 142.71200000000002 L 416.2125128286856 134.67200000000003 C 416.2125128286856 134.67200000000003 416.2125128286856 134.67200000000003 416.2125128286856 134.67200000000003 L 425.7806165718738 134.67200000000003 C 425.7806165718738 134.67200000000003 425.7806165718738 134.67200000000003 425.7806165718738 134.67200000000003 L 425.7806165718738 142.71200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 416.2125128286856 142.71200000000002 L 416.2125128286856 134.67200000000003 C 416.2125128286856 134.67200000000003 416.2125128286856 134.67200000000003 416.2125128286856 134.67200000000003 L 425.7806165718738 134.67200000000003 C 425.7806165718738 134.67200000000003 425.7806165718738 134.67200000000003 425.7806165718738 134.67200000000003 L 425.7806165718738 142.71200000000002 z " pathFrom="M 416.2125128286856 142.71200000000002 L 416.2125128286856 142.71200000000002 L 425.7806165718738 142.71200000000002 L 425.7806165718738 142.71200000000002 L 425.7806165718738 142.71200000000002 L 425.7806165718738 142.71200000000002 L 425.7806165718738 142.71200000000002 L 416.2125128286856 142.71200000000002 z" cy="134.67100000000002" cx="425.7806165718738" j="22" val="4" barHeight="8.04" barWidth="9.568103743188175"></path><path id="SvgjsPath5739" d="M 435.34872031506194 98.49200000000002 L 435.34872031506194 86.43200000000002 C 435.34872031506194 86.43200000000002 435.34872031506194 86.43200000000002 435.34872031506194 86.43200000000002 L 444.9168240582501 86.43200000000002 C 444.9168240582501 86.43200000000002 444.9168240582501 86.43200000000002 444.9168240582501 86.43200000000002 L 444.9168240582501 98.49200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 435.34872031506194 98.49200000000002 L 435.34872031506194 86.43200000000002 C 435.34872031506194 86.43200000000002 435.34872031506194 86.43200000000002 435.34872031506194 86.43200000000002 L 444.9168240582501 86.43200000000002 C 444.9168240582501 86.43200000000002 444.9168240582501 86.43200000000002 444.9168240582501 86.43200000000002 L 444.9168240582501 98.49200000000002 z " pathFrom="M 435.34872031506194 98.49200000000002 L 435.34872031506194 98.49200000000002 L 444.9168240582501 98.49200000000002 L 444.9168240582501 98.49200000000002 L 444.9168240582501 98.49200000000002 L 444.9168240582501 98.49200000000002 L 444.9168240582501 98.49200000000002 L 435.34872031506194 98.49200000000002 z" cy="86.43100000000001" cx="444.9168240582501" j="23" val="6" barHeight="12.06" barWidth="9.568103743188175"></path><path id="SvgjsPath5741" d="M 454.4849278014383 120.60200000000002 L 454.4849278014383 84.42200000000003 C 454.4849278014383 84.42200000000003 454.4849278014383 84.42200000000003 454.4849278014383 84.42200000000003 L 464.0530315446265 84.42200000000003 C 464.0530315446265 84.42200000000003 464.0530315446265 84.42200000000003 464.0530315446265 84.42200000000003 L 464.0530315446265 120.60200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 454.4849278014383 120.60200000000002 L 454.4849278014383 84.42200000000003 C 454.4849278014383 84.42200000000003 454.4849278014383 84.42200000000003 454.4849278014383 84.42200000000003 L 464.0530315446265 84.42200000000003 C 464.0530315446265 84.42200000000003 464.0530315446265 84.42200000000003 464.0530315446265 84.42200000000003 L 464.0530315446265 120.60200000000002 z " pathFrom="M 454.4849278014383 120.60200000000002 L 454.4849278014383 120.60200000000002 L 464.0530315446265 120.60200000000002 L 464.0530315446265 120.60200000000002 L 464.0530315446265 120.60200000000002 L 464.0530315446265 120.60200000000002 L 464.0530315446265 120.60200000000002 L 454.4849278014383 120.60200000000002 z" cy="84.42100000000002" cx="464.0530315446265" j="24" val="18" barHeight="36.18" barWidth="9.568103743188175"></path><path id="SvgjsPath5743" d="M 473.62113528781464 106.53200000000001 L 473.62113528781464 100.50200000000001 C 473.62113528781464 100.50200000000001 473.62113528781464 100.50200000000001 473.62113528781464 100.50200000000001 L 483.1892390310028 100.50200000000001 C 483.1892390310028 100.50200000000001 483.1892390310028 100.50200000000001 483.1892390310028 100.50200000000001 L 483.1892390310028 106.53200000000001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 473.62113528781464 106.53200000000001 L 473.62113528781464 100.50200000000001 C 473.62113528781464 100.50200000000001 473.62113528781464 100.50200000000001 473.62113528781464 100.50200000000001 L 483.1892390310028 100.50200000000001 C 483.1892390310028 100.50200000000001 483.1892390310028 100.50200000000001 483.1892390310028 100.50200000000001 L 483.1892390310028 106.53200000000001 z " pathFrom="M 473.62113528781464 106.53200000000001 L 473.62113528781464 106.53200000000001 L 483.1892390310028 106.53200000000001 L 483.1892390310028 106.53200000000001 L 483.1892390310028 106.53200000000001 L 483.1892390310028 106.53200000000001 L 483.1892390310028 106.53200000000001 L 473.62113528781464 106.53200000000001 z" cy="100.501" cx="483.1892390310028" j="25" val="3" barHeight="6.03" barWidth="9.568103743188175"></path><path id="SvgjsPath5745" d="M 492.757342774191 154.77200000000002 L 492.757342774191 144.722 C 492.757342774191 144.722 492.757342774191 144.722 492.757342774191 144.722 L 502.3254465173792 144.722 C 502.3254465173792 144.722 502.3254465173792 144.722 502.3254465173792 144.722 L 502.3254465173792 154.77200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 492.757342774191 154.77200000000002 L 492.757342774191 144.722 C 492.757342774191 144.722 492.757342774191 144.722 492.757342774191 144.722 L 502.3254465173792 144.722 C 502.3254465173792 144.722 502.3254465173792 144.722 502.3254465173792 144.722 L 502.3254465173792 154.77200000000002 z " pathFrom="M 492.757342774191 154.77200000000002 L 492.757342774191 154.77200000000002 L 502.3254465173792 154.77200000000002 L 502.3254465173792 154.77200000000002 L 502.3254465173792 154.77200000000002 L 502.3254465173792 154.77200000000002 L 502.3254465173792 154.77200000000002 L 492.757342774191 154.77200000000002 z" cy="144.721" cx="502.3254465173792" j="26" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5747" d="M 511.8935502605673 148.74200000000002 L 511.8935502605673 144.722 C 511.8935502605673 144.722 511.8935502605673 144.722 511.8935502605673 144.722 L 521.4616540037555 144.722 C 521.4616540037555 144.722 521.4616540037555 144.722 521.4616540037555 144.722 L 521.4616540037555 148.74200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 511.8935502605673 148.74200000000002 L 511.8935502605673 144.722 C 511.8935502605673 144.722 511.8935502605673 144.722 511.8935502605673 144.722 L 521.4616540037555 144.722 C 521.4616540037555 144.722 521.4616540037555 144.722 521.4616540037555 144.722 L 521.4616540037555 148.74200000000002 z " pathFrom="M 511.8935502605673 148.74200000000002 L 511.8935502605673 148.74200000000002 L 521.4616540037555 148.74200000000002 L 521.4616540037555 148.74200000000002 L 521.4616540037555 148.74200000000002 L 521.4616540037555 148.74200000000002 L 521.4616540037555 148.74200000000002 L 511.8935502605673 148.74200000000002 z" cy="144.721" cx="521.4616540037555" j="27" val="2" barHeight="4.02" barWidth="9.568103743188175"></path><path id="SvgjsPath5749" d="M 531.0297577469437 100.50200000000001 L 531.0297577469437 74.37200000000001 C 531.0297577469437 74.37200000000001 531.0297577469437 74.37200000000001 531.0297577469437 74.37200000000001 L 540.5978614901319 74.37200000000001 C 540.5978614901319 74.37200000000001 540.5978614901319 74.37200000000001 540.5978614901319 74.37200000000001 L 540.5978614901319 100.50200000000001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 531.0297577469437 100.50200000000001 L 531.0297577469437 74.37200000000001 C 531.0297577469437 74.37200000000001 531.0297577469437 74.37200000000001 531.0297577469437 74.37200000000001 L 540.5978614901319 74.37200000000001 C 540.5978614901319 74.37200000000001 540.5978614901319 74.37200000000001 540.5978614901319 74.37200000000001 L 540.5978614901319 100.50200000000001 z " pathFrom="M 531.0297577469437 100.50200000000001 L 531.0297577469437 100.50200000000001 L 540.5978614901319 100.50200000000001 L 540.5978614901319 100.50200000000001 L 540.5978614901319 100.50200000000001 L 540.5978614901319 100.50200000000001 L 540.5978614901319 100.50200000000001 L 531.0297577469437 100.50200000000001 z" cy="74.37100000000001" cx="540.5978614901319" j="28" val="13" barHeight="26.13" barWidth="9.568103743188175"></path><path id="SvgjsPath5751" d="M 550.16596523332 148.74200000000002 L 550.16596523332 118.59200000000001 C 550.16596523332 118.59200000000001 550.16596523332 118.59200000000001 550.16596523332 118.59200000000001 L 559.7340689765082 118.59200000000001 C 559.7340689765082 118.59200000000001 559.7340689765082 118.59200000000001 559.7340689765082 118.59200000000001 L 559.7340689765082 148.74200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 550.16596523332 148.74200000000002 L 550.16596523332 118.59200000000001 C 550.16596523332 118.59200000000001 550.16596523332 118.59200000000001 550.16596523332 118.59200000000001 L 559.7340689765082 118.59200000000001 C 559.7340689765082 118.59200000000001 559.7340689765082 118.59200000000001 559.7340689765082 118.59200000000001 L 559.7340689765082 148.74200000000002 z " pathFrom="M 550.16596523332 148.74200000000002 L 550.16596523332 148.74200000000002 L 559.7340689765082 148.74200000000002 L 559.7340689765082 148.74200000000002 L 559.7340689765082 148.74200000000002 L 559.7340689765082 148.74200000000002 L 559.7340689765082 148.74200000000002 L 550.16596523332 148.74200000000002 z" cy="118.59100000000001" cx="559.7340689765082" j="29" val="15" barHeight="30.15" barWidth="9.568103743188175"></path><path id="SvgjsPath5753" d="M 569.3021727196964 118.59200000000001 L 569.3021727196964 78.39200000000002 C 569.3021727196964 78.39200000000002 569.3021727196964 78.39200000000002 569.3021727196964 78.39200000000002 L 578.8702764628846 78.39200000000002 C 578.8702764628846 78.39200000000002 578.8702764628846 78.39200000000002 578.8702764628846 78.39200000000002 L 578.8702764628846 118.59200000000001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 569.3021727196964 118.59200000000001 L 569.3021727196964 78.39200000000002 C 569.3021727196964 78.39200000000002 569.3021727196964 78.39200000000002 569.3021727196964 78.39200000000002 L 578.8702764628846 78.39200000000002 C 578.8702764628846 78.39200000000002 578.8702764628846 78.39200000000002 578.8702764628846 78.39200000000002 L 578.8702764628846 118.59200000000001 z " pathFrom="M 569.3021727196964 118.59200000000001 L 569.3021727196964 118.59200000000001 L 578.8702764628846 118.59200000000001 L 578.8702764628846 118.59200000000001 L 578.8702764628846 118.59200000000001 L 578.8702764628846 118.59200000000001 L 578.8702764628846 118.59200000000001 L 569.3021727196964 118.59200000000001 z" cy="78.39100000000002" cx="578.8702764628846" j="30" val="20" barHeight="40.199999999999996" barWidth="9.568103743188175"></path><path id="SvgjsPath5755" d="M 588.4383802060727 156.782 L 588.4383802060727 62.312000000000005 C 588.4383802060727 62.312000000000005 588.4383802060727 62.312000000000005 588.4383802060727 62.312000000000005 L 598.0064839492609 62.312000000000005 C 598.0064839492609 62.312000000000005 598.0064839492609 62.312000000000005 598.0064839492609 62.312000000000005 L 598.0064839492609 156.782 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 588.4383802060727 156.782 L 588.4383802060727 62.312000000000005 C 588.4383802060727 62.312000000000005 588.4383802060727 62.312000000000005 588.4383802060727 62.312000000000005 L 598.0064839492609 62.312000000000005 C 598.0064839492609 62.312000000000005 598.0064839492609 62.312000000000005 598.0064839492609 62.312000000000005 L 598.0064839492609 156.782 z " pathFrom="M 588.4383802060727 156.782 L 588.4383802060727 156.782 L 598.0064839492609 156.782 L 598.0064839492609 156.782 L 598.0064839492609 156.782 L 598.0064839492609 156.782 L 598.0064839492609 156.782 L 588.4383802060727 156.782 z" cy="62.31100000000001" cx="598.0064839492609" j="31" val="47" barHeight="94.47" barWidth="9.568103743188175"></path><path id="SvgjsPath5757" d="M 607.5745876924491 108.54200000000002 L 607.5745876924491 72.36200000000002 C 607.5745876924491 72.36200000000002 607.5745876924491 72.36200000000002 607.5745876924491 72.36200000000002 L 617.1426914356373 72.36200000000002 C 617.1426914356373 72.36200000000002 617.1426914356373 72.36200000000002 617.1426914356373 72.36200000000002 L 617.1426914356373 108.54200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 607.5745876924491 108.54200000000002 L 607.5745876924491 72.36200000000002 C 607.5745876924491 72.36200000000002 607.5745876924491 72.36200000000002 607.5745876924491 72.36200000000002 L 617.1426914356373 72.36200000000002 C 617.1426914356373 72.36200000000002 617.1426914356373 72.36200000000002 617.1426914356373 72.36200000000002 L 617.1426914356373 108.54200000000002 z " pathFrom="M 607.5745876924491 108.54200000000002 L 607.5745876924491 108.54200000000002 L 617.1426914356373 108.54200000000002 L 617.1426914356373 108.54200000000002 L 617.1426914356373 108.54200000000002 L 617.1426914356373 108.54200000000002 L 617.1426914356373 108.54200000000002 L 607.5745876924491 108.54200000000002 z" cy="72.36100000000002" cx="617.1426914356373" j="32" val="18" barHeight="36.18" barWidth="9.568103743188175"></path><path id="SvgjsPath5759" d="M 626.7107951788254 106.53200000000001 L 626.7107951788254 76.382 C 626.7107951788254 76.382 626.7107951788254 76.382 626.7107951788254 76.382 L 636.2788989220136 76.382 C 636.2788989220136 76.382 636.2788989220136 76.382 636.2788989220136 76.382 L 636.2788989220136 106.53200000000001 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 626.7107951788254 106.53200000000001 L 626.7107951788254 76.382 C 626.7107951788254 76.382 626.7107951788254 76.382 626.7107951788254 76.382 L 636.2788989220136 76.382 C 636.2788989220136 76.382 636.2788989220136 76.382 636.2788989220136 76.382 L 636.2788989220136 106.53200000000001 z " pathFrom="M 626.7107951788254 106.53200000000001 L 626.7107951788254 106.53200000000001 L 636.2788989220136 106.53200000000001 L 636.2788989220136 106.53200000000001 L 636.2788989220136 106.53200000000001 L 636.2788989220136 106.53200000000001 L 636.2788989220136 106.53200000000001 L 626.7107951788254 106.53200000000001 z" cy="76.381" cx="636.2788989220136" j="33" val="15" barHeight="30.15" barWidth="9.568103743188175"></path><path id="SvgjsPath5761" d="M 645.8470026652018 38.19199999999999 L 645.8470026652018 16.081999999999997 C 645.8470026652018 16.081999999999997 645.8470026652018 16.081999999999997 645.8470026652018 16.081999999999997 L 655.41510640839 16.081999999999997 C 655.41510640839 16.081999999999997 655.41510640839 16.081999999999997 655.41510640839 16.081999999999997 L 655.41510640839 38.19199999999999 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 645.8470026652018 38.19199999999999 L 645.8470026652018 16.081999999999997 C 645.8470026652018 16.081999999999997 645.8470026652018 16.081999999999997 645.8470026652018 16.081999999999997 L 655.41510640839 16.081999999999997 C 655.41510640839 16.081999999999997 655.41510640839 16.081999999999997 655.41510640839 16.081999999999997 L 655.41510640839 38.19199999999999 z " pathFrom="M 645.8470026652018 38.19199999999999 L 645.8470026652018 38.19199999999999 L 655.41510640839 38.19199999999999 L 655.41510640839 38.19199999999999 L 655.41510640839 38.19199999999999 L 655.41510640839 38.19199999999999 L 655.41510640839 38.19199999999999 L 645.8470026652018 38.19199999999999 z" cy="16.080999999999996" cx="655.41510640839" j="34" val="11" barHeight="22.11" barWidth="9.568103743188175"></path><path id="SvgjsPath5763" d="M 664.9832101515781 108.54200000000002 L 664.9832101515781 88.44200000000002 C 664.9832101515781 88.44200000000002 664.9832101515781 88.44200000000002 664.9832101515781 88.44200000000002 L 674.5513138947663 88.44200000000002 C 674.5513138947663 88.44200000000002 674.5513138947663 88.44200000000002 674.5513138947663 88.44200000000002 L 674.5513138947663 108.54200000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-primary) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 664.9832101515781 108.54200000000002 L 664.9832101515781 88.44200000000002 C 664.9832101515781 88.44200000000002 664.9832101515781 88.44200000000002 664.9832101515781 88.44200000000002 L 674.5513138947663 88.44200000000002 C 674.5513138947663 88.44200000000002 674.5513138947663 88.44200000000002 674.5513138947663 88.44200000000002 L 674.5513138947663 108.54200000000002 z " pathFrom="M 664.9832101515781 108.54200000000002 L 664.9832101515781 108.54200000000002 L 674.5513138947663 108.54200000000002 L 674.5513138947663 108.54200000000002 L 674.5513138947663 108.54200000000002 L 674.5513138947663 108.54200000000002 L 674.5513138947663 108.54200000000002 L 664.9832101515781 108.54200000000002 z" cy="88.44100000000002" cx="674.5513138947663" j="35" val="10" barHeight="20.099999999999998" barWidth="9.568103743188175"></path><path id="SvgjsPath5765" d="M 0 201" fill="none" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="1" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 684.1194176379545 188.942 L NaN NaN C NaN NaN 684.1194176379545 188.942 684.1194176379545 188.942 L 693.6875213811427 188.942 C 693.6875213811427 188.942 NaN NaN NaN NaN L 693.6875213811427 188.942 z " pathFrom="M 684.1194176379545 188.942 L 684.1194176379545 188.942 L 693.6875213811427 188.942 L 693.6875213811427 188.942 L 693.6875213811427 188.942 L 693.6875213811427 188.942 L 693.6875213811427 188.942 L 684.1194176379545 188.942 z" cy="188.941" cx="693.6875213811427" j="36" val="0" barHeight="0" barWidth="9.568103743188175"></path><g id="SvgjsG5691" class="apexcharts-bar-goals-markers"><g id="SvgjsG5692" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5694" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5696" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5698" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5700" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5702" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5704" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5706" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5708" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5710" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5712" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5714" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5716" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5718" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5720" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5722" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5724" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5726" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5728" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5730" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5732" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5734" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5736" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5738" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5740" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5742" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5744" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5746" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5748" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5750" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5752" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5754" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5756" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5758" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5760" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5762" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5764" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g></g></g><g id="SvgjsG5766" class="apexcharts-series" seriesName="Other" rel="3" data:realIndex="2"><path id="SvgjsPath5770" d="M -4.784051871594087 194.973 L -4.784051871594087 190.953 C -4.784051871594087 190.953 -4.784051871594087 190.953 -4.784051871594087 190.953 L 4.784051871594087 190.953 C 4.784051871594087 190.953 4.784051871594087 190.953 4.784051871594087 190.953 L 4.784051871594087 194.973 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M -4.784051871594087 194.973 L -4.784051871594087 190.953 C -4.784051871594087 190.953 -4.784051871594087 190.953 -4.784051871594087 190.953 L 4.784051871594087 190.953 C 4.784051871594087 190.953 4.784051871594087 190.953 4.784051871594087 190.953 L 4.784051871594087 194.973 z " pathFrom="M -4.784051871594087 194.973 L -4.784051871594087 194.973 L 4.784051871594087 194.973 L 4.784051871594087 194.973 L 4.784051871594087 194.973 L 4.784051871594087 194.973 L 4.784051871594087 194.973 L -4.784051871594087 194.973 z" cy="190.952" cx="4.784051871594087" j="0" val="2" barHeight="4.02" barWidth="9.568103743188175"></path><path id="SvgjsPath5772" d="M 14.352155614782262 190.953 L 14.352155614782262 172.863 C 14.352155614782262 172.863 14.352155614782262 172.863 14.352155614782262 172.863 L 23.920259357970437 172.863 C 23.920259357970437 172.863 23.920259357970437 172.863 23.920259357970437 172.863 L 23.920259357970437 190.953 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 14.352155614782262 190.953 L 14.352155614782262 172.863 C 14.352155614782262 172.863 14.352155614782262 172.863 14.352155614782262 172.863 L 23.920259357970437 172.863 C 23.920259357970437 172.863 23.920259357970437 172.863 23.920259357970437 172.863 L 23.920259357970437 190.953 z " pathFrom="M 14.352155614782262 190.953 L 14.352155614782262 190.953 L 23.920259357970437 190.953 L 23.920259357970437 190.953 L 23.920259357970437 190.953 L 23.920259357970437 190.953 L 23.920259357970437 190.953 L 14.352155614782262 190.953 z" cy="172.862" cx="23.920259357970437" j="1" val="9" barHeight="18.09" barWidth="9.568103743188175"></path><path id="SvgjsPath5774" d="M 33.48836310115861 192.96300000000002 L 33.48836310115861 190.95300000000003 C 33.48836310115861 190.95300000000003 33.48836310115861 190.95300000000003 33.48836310115861 190.95300000000003 L 43.05646684434679 190.95300000000003 C 43.05646684434679 190.95300000000003 43.05646684434679 190.95300000000003 43.05646684434679 190.95300000000003 L 43.05646684434679 192.96300000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 33.48836310115861 192.96300000000002 L 33.48836310115861 190.95300000000003 C 33.48836310115861 190.95300000000003 33.48836310115861 190.95300000000003 33.48836310115861 190.95300000000003 L 43.05646684434679 190.95300000000003 C 43.05646684434679 190.95300000000003 43.05646684434679 190.95300000000003 43.05646684434679 190.95300000000003 L 43.05646684434679 192.96300000000002 z " pathFrom="M 33.48836310115861 192.96300000000002 L 33.48836310115861 192.96300000000002 L 43.05646684434679 192.96300000000002 L 43.05646684434679 192.96300000000002 L 43.05646684434679 192.96300000000002 L 43.05646684434679 192.96300000000002 L 43.05646684434679 192.96300000000002 L 33.48836310115861 192.96300000000002 z" cy="190.95200000000003" cx="43.05646684434679" j="2" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5776" d="M 52.62457058753496 194.973 L 52.62457058753496 180.90300000000002 C 52.62457058753496 180.90300000000002 52.62457058753496 180.90300000000002 52.62457058753496 180.90300000000002 L 62.192674330723136 180.90300000000002 C 62.192674330723136 180.90300000000002 62.192674330723136 180.90300000000002 62.192674330723136 180.90300000000002 L 62.192674330723136 194.973 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 52.62457058753496 194.973 L 52.62457058753496 180.90300000000002 C 52.62457058753496 180.90300000000002 52.62457058753496 180.90300000000002 52.62457058753496 180.90300000000002 L 62.192674330723136 180.90300000000002 C 62.192674330723136 180.90300000000002 62.192674330723136 180.90300000000002 62.192674330723136 180.90300000000002 L 62.192674330723136 194.973 z " pathFrom="M 52.62457058753496 194.973 L 52.62457058753496 194.973 L 62.192674330723136 194.973 L 62.192674330723136 194.973 L 62.192674330723136 194.973 L 62.192674330723136 194.973 L 62.192674330723136 194.973 L 52.62457058753496 194.973 z" cy="180.90200000000002" cx="62.192674330723136" j="3" val="7" barHeight="14.07" barWidth="9.568103743188175"></path><path id="SvgjsPath5778" d="M 71.76077807391131 194.973 L 71.76077807391131 178.893 C 71.76077807391131 178.893 71.76077807391131 178.893 71.76077807391131 178.893 L 81.32888181709949 178.893 C 81.32888181709949 178.893 81.32888181709949 178.893 81.32888181709949 178.893 L 81.32888181709949 194.973 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 71.76077807391131 194.973 L 71.76077807391131 178.893 C 71.76077807391131 178.893 71.76077807391131 178.893 71.76077807391131 178.893 L 81.32888181709949 178.893 C 81.32888181709949 178.893 81.32888181709949 178.893 81.32888181709949 178.893 L 81.32888181709949 194.973 z " pathFrom="M 71.76077807391131 194.973 L 71.76077807391131 194.973 L 81.32888181709949 194.973 L 81.32888181709949 194.973 L 81.32888181709949 194.973 L 81.32888181709949 194.973 L 81.32888181709949 194.973 L 71.76077807391131 194.973 z" cy="178.892" cx="81.32888181709949" j="4" val="8" barHeight="16.08" barWidth="9.568103743188175"></path><path id="SvgjsPath5780" d="M 90.89698556028766 196.98300000000003 L 90.89698556028766 190.95300000000003 C 90.89698556028766 190.95300000000003 90.89698556028766 190.95300000000003 90.89698556028766 190.95300000000003 L 100.46508930347584 190.95300000000003 C 100.46508930347584 190.95300000000003 100.46508930347584 190.95300000000003 100.46508930347584 190.95300000000003 L 100.46508930347584 196.98300000000003 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 90.89698556028766 196.98300000000003 L 90.89698556028766 190.95300000000003 C 90.89698556028766 190.95300000000003 90.89698556028766 190.95300000000003 90.89698556028766 190.95300000000003 L 100.46508930347584 190.95300000000003 C 100.46508930347584 190.95300000000003 100.46508930347584 190.95300000000003 100.46508930347584 190.95300000000003 L 100.46508930347584 196.98300000000003 z " pathFrom="M 90.89698556028766 196.98300000000003 L 90.89698556028766 196.98300000000003 L 100.46508930347584 196.98300000000003 L 100.46508930347584 196.98300000000003 L 100.46508930347584 196.98300000000003 L 100.46508930347584 196.98300000000003 L 100.46508930347584 196.98300000000003 L 90.89698556028766 196.98300000000003 z" cy="190.95200000000003" cx="100.46508930347584" j="5" val="3" barHeight="6.03" barWidth="9.568103743188175"></path><path id="SvgjsPath5782" d="M 110.03319304666401 190.95300000000003 L 110.03319304666401 178.89300000000003 C 110.03319304666401 178.89300000000003 110.03319304666401 178.89300000000003 110.03319304666401 178.89300000000003 L 119.60129678985219 178.89300000000003 C 119.60129678985219 178.89300000000003 119.60129678985219 178.89300000000003 119.60129678985219 178.89300000000003 L 119.60129678985219 190.95300000000003 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 110.03319304666401 190.95300000000003 L 110.03319304666401 178.89300000000003 C 110.03319304666401 178.89300000000003 110.03319304666401 178.89300000000003 110.03319304666401 178.89300000000003 L 119.60129678985219 178.89300000000003 C 119.60129678985219 178.89300000000003 119.60129678985219 178.89300000000003 119.60129678985219 178.89300000000003 L 119.60129678985219 190.95300000000003 z " pathFrom="M 110.03319304666401 190.95300000000003 L 110.03319304666401 190.95300000000003 L 119.60129678985219 190.95300000000003 L 119.60129678985219 190.95300000000003 L 119.60129678985219 190.95300000000003 L 119.60129678985219 190.95300000000003 L 119.60129678985219 190.95300000000003 L 110.03319304666401 190.95300000000003 z" cy="178.89200000000002" cx="119.60129678985219" j="6" val="6" barHeight="12.06" barWidth="9.568103743188175"></path><path id="SvgjsPath5784" d="M 129.16940053304035 186.93300000000002 L 129.16940053304035 176.883 C 129.16940053304035 176.883 129.16940053304035 176.883 129.16940053304035 176.883 L 138.73750427622852 176.883 C 138.73750427622852 176.883 138.73750427622852 176.883 138.73750427622852 176.883 L 138.73750427622852 186.93300000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 129.16940053304035 186.93300000000002 L 129.16940053304035 176.883 C 129.16940053304035 176.883 129.16940053304035 176.883 129.16940053304035 176.883 L 138.73750427622852 176.883 C 138.73750427622852 176.883 138.73750427622852 176.883 138.73750427622852 176.883 L 138.73750427622852 186.93300000000002 z " pathFrom="M 129.16940053304035 186.93300000000002 L 129.16940053304035 186.93300000000002 L 138.73750427622852 186.93300000000002 L 138.73750427622852 186.93300000000002 L 138.73750427622852 186.93300000000002 L 138.73750427622852 186.93300000000002 L 138.73750427622852 186.93300000000002 L 129.16940053304035 186.93300000000002 z" cy="176.882" cx="138.73750427622852" j="7" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5786" d="M 148.3056080194167 190.953 L 148.3056080194167 180.903 C 148.3056080194167 180.903 148.3056080194167 180.903 148.3056080194167 180.903 L 157.87371176260487 180.903 C 157.87371176260487 180.903 157.87371176260487 180.903 157.87371176260487 180.903 L 157.87371176260487 190.953 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 148.3056080194167 190.953 L 148.3056080194167 180.903 C 148.3056080194167 180.903 148.3056080194167 180.903 148.3056080194167 180.903 L 157.87371176260487 180.903 C 157.87371176260487 180.903 157.87371176260487 180.903 157.87371176260487 180.903 L 157.87371176260487 190.953 z " pathFrom="M 148.3056080194167 190.953 L 148.3056080194167 190.953 L 157.87371176260487 190.953 L 157.87371176260487 190.953 L 157.87371176260487 190.953 L 157.87371176260487 190.953 L 157.87371176260487 190.953 L 148.3056080194167 190.953 z" cy="180.902" cx="157.87371176260487" j="8" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5788" d="M 167.44181550579304 198.99300000000002 L 167.44181550579304 190.95300000000003 C 167.44181550579304 190.95300000000003 167.44181550579304 190.95300000000003 167.44181550579304 190.95300000000003 L 177.00991924898122 190.95300000000003 C 177.00991924898122 190.95300000000003 177.00991924898122 190.95300000000003 177.00991924898122 190.95300000000003 L 177.00991924898122 198.99300000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 167.44181550579304 198.99300000000002 L 167.44181550579304 190.95300000000003 C 167.44181550579304 190.95300000000003 167.44181550579304 190.95300000000003 167.44181550579304 190.95300000000003 L 177.00991924898122 190.95300000000003 C 177.00991924898122 190.95300000000003 177.00991924898122 190.95300000000003 177.00991924898122 190.95300000000003 L 177.00991924898122 198.99300000000002 z " pathFrom="M 167.44181550579304 198.99300000000002 L 167.44181550579304 198.99300000000002 L 177.00991924898122 198.99300000000002 L 177.00991924898122 198.99300000000002 L 177.00991924898122 198.99300000000002 L 177.00991924898122 198.99300000000002 L 177.00991924898122 198.99300000000002 L 167.44181550579304 198.99300000000002 z" cy="190.95200000000003" cx="177.00991924898122" j="9" val="4" barHeight="8.04" barWidth="9.568103743188175"></path><path id="SvgjsPath5790" d="M 186.5780229921694 192.963 L 186.5780229921694 180.903 C 186.5780229921694 180.903 186.5780229921694 180.903 186.5780229921694 180.903 L 196.14612673535757 180.903 C 196.14612673535757 180.903 196.14612673535757 180.903 196.14612673535757 180.903 L 196.14612673535757 192.963 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 186.5780229921694 192.963 L 186.5780229921694 180.903 C 186.5780229921694 180.903 186.5780229921694 180.903 186.5780229921694 180.903 L 196.14612673535757 180.903 C 196.14612673535757 180.903 196.14612673535757 180.903 196.14612673535757 180.903 L 196.14612673535757 192.963 z " pathFrom="M 186.5780229921694 192.963 L 186.5780229921694 192.963 L 196.14612673535757 192.963 L 196.14612673535757 192.963 L 196.14612673535757 192.963 L 196.14612673535757 192.963 L 196.14612673535757 192.963 L 186.5780229921694 192.963 z" cy="180.902" cx="196.14612673535757" j="10" val="6" barHeight="12.06" barWidth="9.568103743188175"></path><path id="SvgjsPath5792" d="M 205.71423047854574 166.833 L 205.71423047854574 158.793 C 205.71423047854574 158.793 205.71423047854574 158.793 205.71423047854574 158.793 L 215.28233422173392 158.793 C 215.28233422173392 158.793 215.28233422173392 158.793 215.28233422173392 158.793 L 215.28233422173392 166.833 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 205.71423047854574 166.833 L 205.71423047854574 158.793 C 205.71423047854574 158.793 205.71423047854574 158.793 205.71423047854574 158.793 L 215.28233422173392 158.793 C 215.28233422173392 158.793 215.28233422173392 158.793 215.28233422173392 158.793 L 215.28233422173392 166.833 z " pathFrom="M 205.71423047854574 166.833 L 205.71423047854574 166.833 L 215.28233422173392 166.833 L 215.28233422173392 166.833 L 215.28233422173392 166.833 L 215.28233422173392 166.833 L 215.28233422173392 166.833 L 205.71423047854574 166.833 z" cy="158.792" cx="215.28233422173392" j="11" val="4" barHeight="8.04" barWidth="9.568103743188175"></path><path id="SvgjsPath5794" d="M 224.8504379649221 184.923 L 224.8504379649221 182.913 C 224.8504379649221 182.913 224.8504379649221 182.913 224.8504379649221 182.913 L 234.41854170811027 182.913 C 234.41854170811027 182.913 234.41854170811027 182.913 234.41854170811027 182.913 L 234.41854170811027 184.923 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 224.8504379649221 184.923 L 224.8504379649221 182.913 C 224.8504379649221 182.913 224.8504379649221 182.913 224.8504379649221 182.913 L 234.41854170811027 182.913 C 234.41854170811027 182.913 234.41854170811027 182.913 234.41854170811027 182.913 L 234.41854170811027 184.923 z " pathFrom="M 224.8504379649221 184.923 L 224.8504379649221 184.923 L 234.41854170811027 184.923 L 234.41854170811027 184.923 L 234.41854170811027 184.923 L 234.41854170811027 184.923 L 234.41854170811027 184.923 L 224.8504379649221 184.923 z" cy="182.912" cx="234.41854170811027" j="12" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5796" d="M 243.98664545129844 180.90300000000002 L 243.98664545129844 162.81300000000002 C 243.98664545129844 162.81300000000002 243.98664545129844 162.81300000000002 243.98664545129844 162.81300000000002 L 253.55474919448662 162.81300000000002 C 253.55474919448662 162.81300000000002 253.55474919448662 162.81300000000002 253.55474919448662 162.81300000000002 L 253.55474919448662 180.90300000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 243.98664545129844 180.90300000000002 L 243.98664545129844 162.81300000000002 C 243.98664545129844 162.81300000000002 243.98664545129844 162.81300000000002 243.98664545129844 162.81300000000002 L 253.55474919448662 162.81300000000002 C 253.55474919448662 162.81300000000002 253.55474919448662 162.81300000000002 253.55474919448662 162.81300000000002 L 253.55474919448662 180.90300000000002 z " pathFrom="M 243.98664545129844 180.90300000000002 L 243.98664545129844 180.90300000000002 L 253.55474919448662 180.90300000000002 L 253.55474919448662 180.90300000000002 L 253.55474919448662 180.90300000000002 L 253.55474919448662 180.90300000000002 L 253.55474919448662 180.90300000000002 L 243.98664545129844 180.90300000000002 z" cy="162.812" cx="253.55474919448662" j="13" val="9" barHeight="18.09" barWidth="9.568103743188175"></path><path id="SvgjsPath5798" d="M 263.1228529376748 144.723 L 263.1228529376748 138.693 C 263.1228529376748 138.693 263.1228529376748 138.693 263.1228529376748 138.693 L 272.690956680863 138.693 C 272.690956680863 138.693 272.690956680863 138.693 272.690956680863 138.693 L 272.690956680863 144.723 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 263.1228529376748 144.723 L 263.1228529376748 138.693 C 263.1228529376748 138.693 263.1228529376748 138.693 263.1228529376748 138.693 L 272.690956680863 138.693 C 272.690956680863 138.693 272.690956680863 138.693 272.690956680863 138.693 L 272.690956680863 144.723 z " pathFrom="M 263.1228529376748 144.723 L 263.1228529376748 144.723 L 272.690956680863 144.723 L 272.690956680863 144.723 L 272.690956680863 144.723 L 272.690956680863 144.723 L 272.690956680863 144.723 L 263.1228529376748 144.723 z" cy="138.692" cx="272.690956680863" j="14" val="3" barHeight="6.03" barWidth="9.568103743188175"></path><path id="SvgjsPath5800" d="M 282.25906042405114 174.87300000000002 L 282.25906042405114 162.81300000000002 C 282.25906042405114 162.81300000000002 282.25906042405114 162.81300000000002 282.25906042405114 162.81300000000002 L 291.8271641672393 162.81300000000002 C 291.8271641672393 162.81300000000002 291.8271641672393 162.81300000000002 291.8271641672393 162.81300000000002 L 291.8271641672393 174.87300000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 282.25906042405114 174.87300000000002 L 282.25906042405114 162.81300000000002 C 282.25906042405114 162.81300000000002 282.25906042405114 162.81300000000002 282.25906042405114 162.81300000000002 L 291.8271641672393 162.81300000000002 C 291.8271641672393 162.81300000000002 291.8271641672393 162.81300000000002 291.8271641672393 162.81300000000002 L 291.8271641672393 174.87300000000002 z " pathFrom="M 282.25906042405114 174.87300000000002 L 282.25906042405114 174.87300000000002 L 291.8271641672393 174.87300000000002 L 291.8271641672393 174.87300000000002 L 291.8271641672393 174.87300000000002 L 291.8271641672393 174.87300000000002 L 291.8271641672393 174.87300000000002 L 282.25906042405114 174.87300000000002 z" cy="162.812" cx="291.8271641672393" j="15" val="6" barHeight="12.06" barWidth="9.568103743188175"></path><path id="SvgjsPath5802" d="M 301.3952679104275 170.85300000000004 L 301.3952679104275 156.78300000000004 C 301.3952679104275 156.78300000000004 301.3952679104275 156.78300000000004 301.3952679104275 156.78300000000004 L 310.9633716536157 156.78300000000004 C 310.9633716536157 156.78300000000004 310.9633716536157 156.78300000000004 310.9633716536157 156.78300000000004 L 310.9633716536157 170.85300000000004 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 301.3952679104275 170.85300000000004 L 301.3952679104275 156.78300000000004 C 301.3952679104275 156.78300000000004 301.3952679104275 156.78300000000004 301.3952679104275 156.78300000000004 L 310.9633716536157 156.78300000000004 C 310.9633716536157 156.78300000000004 310.9633716536157 156.78300000000004 310.9633716536157 156.78300000000004 L 310.9633716536157 170.85300000000004 z " pathFrom="M 301.3952679104275 170.85300000000004 L 301.3952679104275 170.85300000000004 L 310.9633716536157 170.85300000000004 L 310.9633716536157 170.85300000000004 L 310.9633716536157 170.85300000000004 L 310.9633716536157 170.85300000000004 L 310.9633716536157 170.85300000000004 L 301.3952679104275 170.85300000000004 z" cy="156.78200000000004" cx="310.9633716536157" j="16" val="7" barHeight="14.07" barWidth="9.568103743188175"></path><path id="SvgjsPath5804" d="M 320.53147539680384 186.93300000000002 L 320.53147539680384 176.883 C 320.53147539680384 176.883 320.53147539680384 176.883 320.53147539680384 176.883 L 330.099579139992 176.883 C 330.099579139992 176.883 330.099579139992 176.883 330.099579139992 176.883 L 330.099579139992 186.93300000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 320.53147539680384 186.93300000000002 L 320.53147539680384 176.883 C 320.53147539680384 176.883 320.53147539680384 176.883 320.53147539680384 176.883 L 330.099579139992 176.883 C 330.099579139992 176.883 330.099579139992 176.883 330.099579139992 176.883 L 330.099579139992 186.93300000000002 z " pathFrom="M 320.53147539680384 186.93300000000002 L 320.53147539680384 186.93300000000002 L 330.099579139992 186.93300000000002 L 330.099579139992 186.93300000000002 L 330.099579139992 186.93300000000002 L 330.099579139992 186.93300000000002 L 330.099579139992 186.93300000000002 L 320.53147539680384 186.93300000000002 z" cy="176.882" cx="330.099579139992" j="17" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5806" d="M 339.6676828831802 182.913 L 339.6676828831802 178.893 C 339.6676828831802 178.893 339.6676828831802 178.893 339.6676828831802 178.893 L 349.2357866263684 178.893 C 349.2357866263684 178.893 349.2357866263684 178.893 349.2357866263684 178.893 L 349.2357866263684 182.913 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 339.6676828831802 182.913 L 339.6676828831802 178.893 C 339.6676828831802 178.893 339.6676828831802 178.893 339.6676828831802 178.893 L 349.2357866263684 178.893 C 349.2357866263684 178.893 349.2357866263684 178.893 349.2357866263684 178.893 L 349.2357866263684 182.913 z " pathFrom="M 339.6676828831802 182.913 L 339.6676828831802 182.913 L 349.2357866263684 182.913 L 349.2357866263684 182.913 L 349.2357866263684 182.913 L 349.2357866263684 182.913 L 349.2357866263684 182.913 L 339.6676828831802 182.913 z" cy="178.892" cx="349.2357866263684" j="18" val="2" barHeight="4.02" barWidth="9.568103743188175"></path><path id="SvgjsPath5808" d="M 358.80389036955654 188.943 L 358.80389036955654 172.86300000000003 C 358.80389036955654 172.86300000000003 358.80389036955654 172.86300000000003 358.80389036955654 172.86300000000003 L 368.3719941127447 172.86300000000003 C 368.3719941127447 172.86300000000003 368.3719941127447 172.86300000000003 368.3719941127447 172.86300000000003 L 368.3719941127447 188.943 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 358.80389036955654 188.943 L 358.80389036955654 172.86300000000003 C 358.80389036955654 172.86300000000003 358.80389036955654 172.86300000000003 358.80389036955654 172.86300000000003 L 368.3719941127447 172.86300000000003 C 368.3719941127447 172.86300000000003 368.3719941127447 172.86300000000003 368.3719941127447 172.86300000000003 L 368.3719941127447 188.943 z " pathFrom="M 358.80389036955654 188.943 L 358.80389036955654 188.943 L 368.3719941127447 188.943 L 368.3719941127447 188.943 L 368.3719941127447 188.943 L 368.3719941127447 188.943 L 368.3719941127447 188.943 L 358.80389036955654 188.943 z" cy="172.86200000000002" cx="368.3719941127447" j="19" val="8" barHeight="16.08" barWidth="9.568103743188175"></path><path id="SvgjsPath5810" d="M 377.9400978559329 180.90300000000002 L 377.9400978559329 172.86300000000003 C 377.9400978559329 172.86300000000003 377.9400978559329 172.86300000000003 377.9400978559329 172.86300000000003 L 387.5082015991211 172.86300000000003 C 387.5082015991211 172.86300000000003 387.5082015991211 172.86300000000003 387.5082015991211 172.86300000000003 L 387.5082015991211 180.90300000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 377.9400978559329 180.90300000000002 L 377.9400978559329 172.86300000000003 C 377.9400978559329 172.86300000000003 377.9400978559329 172.86300000000003 377.9400978559329 172.86300000000003 L 387.5082015991211 172.86300000000003 C 387.5082015991211 172.86300000000003 387.5082015991211 172.86300000000003 387.5082015991211 172.86300000000003 L 387.5082015991211 180.90300000000002 z " pathFrom="M 377.9400978559329 180.90300000000002 L 377.9400978559329 180.90300000000002 L 387.5082015991211 180.90300000000002 L 387.5082015991211 180.90300000000002 L 387.5082015991211 180.90300000000002 L 387.5082015991211 180.90300000000002 L 387.5082015991211 180.90300000000002 L 377.9400978559329 180.90300000000002 z" cy="172.86200000000002" cx="387.5082015991211" j="20" val="4" barHeight="8.04" barWidth="9.568103743188175"></path><path id="SvgjsPath5812" d="M 397.07630534230924 128.643 L 397.07630534230924 110.553 C 397.07630534230924 110.553 397.07630534230924 110.553 397.07630534230924 110.553 L 406.6444090854974 110.553 C 406.6444090854974 110.553 406.6444090854974 110.553 406.6444090854974 110.553 L 406.6444090854974 128.643 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 397.07630534230924 128.643 L 397.07630534230924 110.553 C 397.07630534230924 110.553 397.07630534230924 110.553 397.07630534230924 110.553 L 406.6444090854974 110.553 C 406.6444090854974 110.553 406.6444090854974 110.553 406.6444090854974 110.553 L 406.6444090854974 128.643 z " pathFrom="M 397.07630534230924 128.643 L 397.07630534230924 128.643 L 406.6444090854974 128.643 L 406.6444090854974 128.643 L 406.6444090854974 128.643 L 406.6444090854974 128.643 L 406.6444090854974 128.643 L 397.07630534230924 128.643 z" cy="110.55199999999999" cx="406.6444090854974" j="21" val="9" barHeight="18.09" barWidth="9.568103743188175"></path><path id="SvgjsPath5814" d="M 416.2125128286856 134.67300000000003 L 416.2125128286856 132.66300000000004 C 416.2125128286856 132.66300000000004 416.2125128286856 132.66300000000004 416.2125128286856 132.66300000000004 L 425.7806165718738 132.66300000000004 C 425.7806165718738 132.66300000000004 425.7806165718738 132.66300000000004 425.7806165718738 132.66300000000004 L 425.7806165718738 134.67300000000003 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 416.2125128286856 134.67300000000003 L 416.2125128286856 132.66300000000004 C 416.2125128286856 132.66300000000004 416.2125128286856 132.66300000000004 416.2125128286856 132.66300000000004 L 425.7806165718738 132.66300000000004 C 425.7806165718738 132.66300000000004 425.7806165718738 132.66300000000004 425.7806165718738 132.66300000000004 L 425.7806165718738 134.67300000000003 z " pathFrom="M 416.2125128286856 134.67300000000003 L 416.2125128286856 134.67300000000003 L 425.7806165718738 134.67300000000003 L 425.7806165718738 134.67300000000003 L 425.7806165718738 134.67300000000003 L 425.7806165718738 134.67300000000003 L 425.7806165718738 134.67300000000003 L 416.2125128286856 134.67300000000003 z" cy="132.66200000000003" cx="425.7806165718738" j="22" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5816" d="M 435.34872031506194 86.43300000000002 L 435.34872031506194 82.41300000000003 C 435.34872031506194 82.41300000000003 435.34872031506194 82.41300000000003 435.34872031506194 82.41300000000003 L 444.9168240582501 82.41300000000003 C 444.9168240582501 82.41300000000003 444.9168240582501 82.41300000000003 444.9168240582501 82.41300000000003 L 444.9168240582501 86.43300000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 435.34872031506194 86.43300000000002 L 435.34872031506194 82.41300000000003 C 435.34872031506194 82.41300000000003 435.34872031506194 82.41300000000003 435.34872031506194 82.41300000000003 L 444.9168240582501 82.41300000000003 C 444.9168240582501 82.41300000000003 444.9168240582501 82.41300000000003 444.9168240582501 82.41300000000003 L 444.9168240582501 86.43300000000002 z " pathFrom="M 435.34872031506194 86.43300000000002 L 435.34872031506194 86.43300000000002 L 444.9168240582501 86.43300000000002 L 444.9168240582501 86.43300000000002 L 444.9168240582501 86.43300000000002 L 444.9168240582501 86.43300000000002 L 444.9168240582501 86.43300000000002 L 435.34872031506194 86.43300000000002 z" cy="82.41200000000002" cx="444.9168240582501" j="23" val="2" barHeight="4.02" barWidth="9.568103743188175"></path><path id="SvgjsPath5818" d="M 454.4849278014383 84.42300000000003 L 454.4849278014383 72.36300000000003 C 454.4849278014383 72.36300000000003 454.4849278014383 72.36300000000003 454.4849278014383 72.36300000000003 L 464.0530315446265 72.36300000000003 C 464.0530315446265 72.36300000000003 464.0530315446265 72.36300000000003 464.0530315446265 72.36300000000003 L 464.0530315446265 84.42300000000003 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 454.4849278014383 84.42300000000003 L 454.4849278014383 72.36300000000003 C 454.4849278014383 72.36300000000003 454.4849278014383 72.36300000000003 454.4849278014383 72.36300000000003 L 464.0530315446265 72.36300000000003 C 464.0530315446265 72.36300000000003 464.0530315446265 72.36300000000003 464.0530315446265 72.36300000000003 L 464.0530315446265 84.42300000000003 z " pathFrom="M 454.4849278014383 84.42300000000003 L 454.4849278014383 84.42300000000003 L 464.0530315446265 84.42300000000003 L 464.0530315446265 84.42300000000003 L 464.0530315446265 84.42300000000003 L 464.0530315446265 84.42300000000003 L 464.0530315446265 84.42300000000003 L 454.4849278014383 84.42300000000003 z" cy="72.36200000000002" cx="464.0530315446265" j="24" val="6" barHeight="12.06" barWidth="9.568103743188175"></path><path id="SvgjsPath5820" d="M 473.62113528781464 100.50300000000001 L 473.62113528781464 86.43300000000002 C 473.62113528781464 86.43300000000002 473.62113528781464 86.43300000000002 473.62113528781464 86.43300000000002 L 483.1892390310028 86.43300000000002 C 483.1892390310028 86.43300000000002 483.1892390310028 86.43300000000002 483.1892390310028 86.43300000000002 L 483.1892390310028 100.50300000000001 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 473.62113528781464 100.50300000000001 L 473.62113528781464 86.43300000000002 C 473.62113528781464 86.43300000000002 473.62113528781464 86.43300000000002 473.62113528781464 86.43300000000002 L 483.1892390310028 86.43300000000002 C 483.1892390310028 86.43300000000002 483.1892390310028 86.43300000000002 483.1892390310028 86.43300000000002 L 483.1892390310028 100.50300000000001 z " pathFrom="M 473.62113528781464 100.50300000000001 L 473.62113528781464 100.50300000000001 L 483.1892390310028 100.50300000000001 L 483.1892390310028 100.50300000000001 L 483.1892390310028 100.50300000000001 L 483.1892390310028 100.50300000000001 L 483.1892390310028 100.50300000000001 L 473.62113528781464 100.50300000000001 z" cy="86.43200000000002" cx="483.1892390310028" j="25" val="7" barHeight="14.07" barWidth="9.568103743188175"></path><path id="SvgjsPath5822" d="M 492.757342774191 144.723 L 492.757342774191 134.673 C 492.757342774191 134.673 492.757342774191 134.673 492.757342774191 134.673 L 502.3254465173792 134.673 C 502.3254465173792 134.673 502.3254465173792 134.673 502.3254465173792 134.673 L 502.3254465173792 144.723 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 492.757342774191 144.723 L 492.757342774191 134.673 C 492.757342774191 134.673 492.757342774191 134.673 492.757342774191 134.673 L 502.3254465173792 134.673 C 502.3254465173792 134.673 502.3254465173792 134.673 502.3254465173792 134.673 L 502.3254465173792 144.723 z " pathFrom="M 492.757342774191 144.723 L 492.757342774191 144.723 L 502.3254465173792 144.723 L 502.3254465173792 144.723 L 502.3254465173792 144.723 L 502.3254465173792 144.723 L 502.3254465173792 144.723 L 492.757342774191 144.723 z" cy="134.672" cx="502.3254465173792" j="26" val="5" barHeight="10.049999999999999" barWidth="9.568103743188175"></path><path id="SvgjsPath5824" d="M 511.8935502605673 144.723 L 511.8935502605673 142.71300000000002 C 511.8935502605673 142.71300000000002 511.8935502605673 142.71300000000002 511.8935502605673 142.71300000000002 L 521.4616540037555 142.71300000000002 C 521.4616540037555 142.71300000000002 521.4616540037555 142.71300000000002 521.4616540037555 142.71300000000002 L 521.4616540037555 144.723 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 511.8935502605673 144.723 L 511.8935502605673 142.71300000000002 C 511.8935502605673 142.71300000000002 511.8935502605673 142.71300000000002 511.8935502605673 142.71300000000002 L 521.4616540037555 142.71300000000002 C 521.4616540037555 142.71300000000002 521.4616540037555 142.71300000000002 521.4616540037555 142.71300000000002 L 521.4616540037555 144.723 z " pathFrom="M 511.8935502605673 144.723 L 511.8935502605673 144.723 L 521.4616540037555 144.723 L 521.4616540037555 144.723 L 521.4616540037555 144.723 L 521.4616540037555 144.723 L 521.4616540037555 144.723 L 511.8935502605673 144.723 z" cy="142.71200000000002" cx="521.4616540037555" j="27" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5826" d="M 531.0297577469437 74.37300000000002 L 531.0297577469437 58.29300000000001 C 531.0297577469437 58.29300000000001 531.0297577469437 58.29300000000001 531.0297577469437 58.29300000000001 L 540.5978614901319 58.29300000000001 C 540.5978614901319 58.29300000000001 540.5978614901319 58.29300000000001 540.5978614901319 58.29300000000001 L 540.5978614901319 74.37300000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 531.0297577469437 74.37300000000002 L 531.0297577469437 58.29300000000001 C 531.0297577469437 58.29300000000001 531.0297577469437 58.29300000000001 531.0297577469437 58.29300000000001 L 540.5978614901319 58.29300000000001 C 540.5978614901319 58.29300000000001 540.5978614901319 58.29300000000001 540.5978614901319 58.29300000000001 L 540.5978614901319 74.37300000000002 z " pathFrom="M 531.0297577469437 74.37300000000002 L 531.0297577469437 74.37300000000002 L 540.5978614901319 74.37300000000002 L 540.5978614901319 74.37300000000002 L 540.5978614901319 74.37300000000002 L 540.5978614901319 74.37300000000002 L 540.5978614901319 74.37300000000002 L 531.0297577469437 74.37300000000002 z" cy="58.292000000000016" cx="540.5978614901319" j="28" val="8" barHeight="16.08" barWidth="9.568103743188175"></path><path id="SvgjsPath5828" d="M 550.16596523332 118.59300000000002 L 550.16596523332 112.56300000000002 C 550.16596523332 112.56300000000002 550.16596523332 112.56300000000002 550.16596523332 112.56300000000002 L 559.7340689765082 112.56300000000002 C 559.7340689765082 112.56300000000002 559.7340689765082 112.56300000000002 559.7340689765082 112.56300000000002 L 559.7340689765082 118.59300000000002 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 550.16596523332 118.59300000000002 L 550.16596523332 112.56300000000002 C 550.16596523332 112.56300000000002 550.16596523332 112.56300000000002 550.16596523332 112.56300000000002 L 559.7340689765082 112.56300000000002 C 559.7340689765082 112.56300000000002 559.7340689765082 112.56300000000002 559.7340689765082 112.56300000000002 L 559.7340689765082 118.59300000000002 z " pathFrom="M 550.16596523332 118.59300000000002 L 550.16596523332 118.59300000000002 L 559.7340689765082 118.59300000000002 L 559.7340689765082 118.59300000000002 L 559.7340689765082 118.59300000000002 L 559.7340689765082 118.59300000000002 L 559.7340689765082 118.59300000000002 L 550.16596523332 118.59300000000002 z" cy="112.56200000000001" cx="559.7340689765082" j="29" val="3" barHeight="6.03" barWidth="9.568103743188175"></path><path id="SvgjsPath5830" d="M 569.3021727196964 78.39300000000003 L 569.3021727196964 74.37300000000003 C 569.3021727196964 74.37300000000003 569.3021727196964 74.37300000000003 569.3021727196964 74.37300000000003 L 578.8702764628846 74.37300000000003 C 578.8702764628846 74.37300000000003 578.8702764628846 74.37300000000003 578.8702764628846 74.37300000000003 L 578.8702764628846 78.39300000000003 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 569.3021727196964 78.39300000000003 L 569.3021727196964 74.37300000000003 C 569.3021727196964 74.37300000000003 569.3021727196964 74.37300000000003 569.3021727196964 74.37300000000003 L 578.8702764628846 74.37300000000003 C 578.8702764628846 74.37300000000003 578.8702764628846 74.37300000000003 578.8702764628846 74.37300000000003 L 578.8702764628846 78.39300000000003 z " pathFrom="M 569.3021727196964 78.39300000000003 L 569.3021727196964 78.39300000000003 L 578.8702764628846 78.39300000000003 L 578.8702764628846 78.39300000000003 L 578.8702764628846 78.39300000000003 L 578.8702764628846 78.39300000000003 L 578.8702764628846 78.39300000000003 L 569.3021727196964 78.39300000000003 z" cy="74.37200000000003" cx="578.8702764628846" j="30" val="2" barHeight="4.02" barWidth="9.568103743188175"></path><path id="SvgjsPath5832" d="M 588.4383802060727 62.313 L 588.4383802060727 56.283 C 588.4383802060727 56.283 588.4383802060727 56.283 588.4383802060727 56.283 L 598.0064839492609 56.283 C 598.0064839492609 56.283 598.0064839492609 56.283 598.0064839492609 56.283 L 598.0064839492609 62.313 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 588.4383802060727 62.313 L 588.4383802060727 56.283 C 588.4383802060727 56.283 588.4383802060727 56.283 588.4383802060727 56.283 L 598.0064839492609 56.283 C 598.0064839492609 56.283 598.0064839492609 56.283 598.0064839492609 56.283 L 598.0064839492609 62.313 z " pathFrom="M 588.4383802060727 62.313 L 588.4383802060727 62.313 L 598.0064839492609 62.313 L 598.0064839492609 62.313 L 598.0064839492609 62.313 L 598.0064839492609 62.313 L 598.0064839492609 62.313 L 588.4383802060727 62.313 z" cy="56.282000000000004" cx="598.0064839492609" j="31" val="3" barHeight="6.03" barWidth="9.568103743188175"></path><path id="SvgjsPath5834" d="M 607.5745876924491 72.36300000000003 L 607.5745876924491 64.32300000000004 C 607.5745876924491 64.32300000000004 607.5745876924491 64.32300000000004 607.5745876924491 64.32300000000004 L 617.1426914356373 64.32300000000004 C 617.1426914356373 64.32300000000004 617.1426914356373 64.32300000000004 617.1426914356373 64.32300000000004 L 617.1426914356373 72.36300000000003 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 607.5745876924491 72.36300000000003 L 607.5745876924491 64.32300000000004 C 607.5745876924491 64.32300000000004 607.5745876924491 64.32300000000004 607.5745876924491 64.32300000000004 L 617.1426914356373 64.32300000000004 C 617.1426914356373 64.32300000000004 617.1426914356373 64.32300000000004 617.1426914356373 64.32300000000004 L 617.1426914356373 72.36300000000003 z " pathFrom="M 607.5745876924491 72.36300000000003 L 607.5745876924491 72.36300000000003 L 617.1426914356373 72.36300000000003 L 617.1426914356373 72.36300000000003 L 617.1426914356373 72.36300000000003 L 617.1426914356373 72.36300000000003 L 617.1426914356373 72.36300000000003 L 607.5745876924491 72.36300000000003 z" cy="64.32200000000003" cx="617.1426914356373" j="32" val="4" barHeight="8.04" barWidth="9.568103743188175"></path><path id="SvgjsPath5836" d="M 626.7107951788254 76.38300000000001 L 626.7107951788254 58.293 C 626.7107951788254 58.293 626.7107951788254 58.293 626.7107951788254 58.293 L 636.2788989220136 58.293 C 636.2788989220136 58.293 636.2788989220136 58.293 636.2788989220136 58.293 L 636.2788989220136 76.38300000000001 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 626.7107951788254 76.38300000000001 L 626.7107951788254 58.293 C 626.7107951788254 58.293 626.7107951788254 58.293 626.7107951788254 58.293 L 636.2788989220136 58.293 C 636.2788989220136 58.293 636.2788989220136 58.293 636.2788989220136 58.293 L 636.2788989220136 76.38300000000001 z " pathFrom="M 626.7107951788254 76.38300000000001 L 626.7107951788254 76.38300000000001 L 636.2788989220136 76.38300000000001 L 636.2788989220136 76.38300000000001 L 636.2788989220136 76.38300000000001 L 636.2788989220136 76.38300000000001 L 636.2788989220136 76.38300000000001 L 626.7107951788254 76.38300000000001 z" cy="58.292" cx="636.2788989220136" j="33" val="9" barHeight="18.09" barWidth="9.568103743188175"></path><path id="SvgjsPath5838" d="M 645.8470026652018 16.083 L 645.8470026652018 2.012999999999997 C 645.8470026652018 2.012999999999997 645.8470026652018 2.012999999999997 645.8470026652018 2.012999999999997 L 655.41510640839 2.012999999999997 C 655.41510640839 2.012999999999997 655.41510640839 2.012999999999997 655.41510640839 2.012999999999997 L 655.41510640839 16.083 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 645.8470026652018 16.083 L 645.8470026652018 2.012999999999997 C 645.8470026652018 2.012999999999997 645.8470026652018 2.012999999999997 645.8470026652018 2.012999999999997 L 655.41510640839 2.012999999999997 C 655.41510640839 2.012999999999997 655.41510640839 2.012999999999997 655.41510640839 2.012999999999997 L 655.41510640839 16.083 z " pathFrom="M 645.8470026652018 16.083 L 645.8470026652018 16.083 L 655.41510640839 16.083 L 655.41510640839 16.083 L 655.41510640839 16.083 L 655.41510640839 16.083 L 655.41510640839 16.083 L 645.8470026652018 16.083 z" cy="2.011999999999997" cx="655.41510640839" j="34" val="7" barHeight="14.07" barWidth="9.568103743188175"></path><path id="SvgjsPath5840" d="M 664.9832101515781 88.44300000000003 L 664.9832101515781 86.43300000000002 C 664.9832101515781 86.43300000000002 664.9832101515781 86.43300000000002 664.9832101515781 86.43300000000002 L 674.5513138947663 86.43300000000002 C 674.5513138947663 86.43300000000002 674.5513138947663 86.43300000000002 674.5513138947663 86.43300000000002 L 674.5513138947663 88.44300000000003 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 664.9832101515781 88.44300000000003 L 664.9832101515781 86.43300000000002 C 664.9832101515781 86.43300000000002 664.9832101515781 86.43300000000002 664.9832101515781 86.43300000000002 L 674.5513138947663 86.43300000000002 C 674.5513138947663 86.43300000000002 674.5513138947663 86.43300000000002 674.5513138947663 86.43300000000002 L 674.5513138947663 88.44300000000003 z " pathFrom="M 664.9832101515781 88.44300000000003 L 664.9832101515781 88.44300000000003 L 674.5513138947663 88.44300000000003 L 674.5513138947663 88.44300000000003 L 674.5513138947663 88.44300000000003 L 674.5513138947663 88.44300000000003 L 674.5513138947663 88.44300000000003 L 664.9832101515781 88.44300000000003 z" cy="86.43200000000002" cx="674.5513138947663" j="35" val="1" barHeight="2.01" barWidth="9.568103743188175"></path><path id="SvgjsPath5842" d="M 684.1194176379545 188.943 L 684.1194176379545 176.883 C 684.1194176379545 176.883 684.1194176379545 176.883 684.1194176379545 176.883 L 693.6875213811427 176.883 C 693.6875213811427 176.883 693.6875213811427 176.883 693.6875213811427 176.883 L 693.6875213811427 188.943 z " fill="color-mix(in srgb, transparent, var(--tblr-green) 80%)" fill-opacity="1" stroke-opacity="1" stroke-linecap="round" stroke-width="0" stroke-dasharray="0" class="apexcharts-bar-area " index="2" clip-path="url(#gridRectBarMaskfndk2ib5)" pathTo="M 684.1194176379545 188.943 L 684.1194176379545 176.883 C 684.1194176379545 176.883 684.1194176379545 176.883 684.1194176379545 176.883 L 693.6875213811427 176.883 C 693.6875213811427 176.883 693.6875213811427 176.883 693.6875213811427 176.883 L 693.6875213811427 188.943 z " pathFrom="M 684.1194176379545 188.943 L 684.1194176379545 188.943 L 693.6875213811427 188.943 L 693.6875213811427 188.943 L 693.6875213811427 188.943 L 693.6875213811427 188.943 L 693.6875213811427 188.943 L 684.1194176379545 188.943 z" cy="176.882" cx="693.6875213811427" j="36" val="6" barHeight="12.06" barWidth="9.568103743188175"></path><g id="SvgjsG5768" class="apexcharts-bar-goals-markers"><g id="SvgjsG5769" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5771" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5773" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5775" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5777" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5779" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5781" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5783" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5785" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5787" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5789" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5791" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5793" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5795" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5797" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5799" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5801" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5803" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5805" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5807" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5809" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5811" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5813" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5815" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5817" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5819" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5821" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5823" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5825" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5827" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5829" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5831" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5833" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5835" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5837" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5839" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g><g id="SvgjsG5841" className="apexcharts-bar-goals-groups" class="apexcharts-hidden-element-shown" clip-path="url(#gridRectMarkerMaskfndk2ib5)"></g></g></g><g id="SvgjsG5613" class="apexcharts-datalabels" data:realIndex="0"></g><g id="SvgjsG5690" class="apexcharts-datalabels" data:realIndex="1"></g><g id="SvgjsG5767" class="apexcharts-datalabels" data:realIndex="2"></g></g><line id="SvgjsLine5865" x1="-9.841478135850695" y1="0" x2="698.7449476453993" y2="0" stroke="#b6b6b6" stroke-dasharray="0" stroke-width="1" stroke-linecap="butt" class="apexcharts-ycrosshairs"></line><line id="SvgjsLine5866" x1="-9.841478135850695" y1="0" x2="698.7449476453993" y2="0" stroke-dasharray="0" stroke-width="0" stroke-linecap="butt" class="apexcharts-ycrosshairs-hidden"></line><g id="SvgjsG5867" class="apexcharts-xaxis" transform="translate(0, 0)"><g id="SvgjsG5868" class="apexcharts-xaxis-texts-g" transform="translate(0, -4)"><text id="SvgjsText5870" font-family="inherit" x="57.40862245912905" y="229" text-anchor="middle" dominant-baseline="auto" font-size="12px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-xaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5871">24 Jun</tspan><title>24 Jun</title></text><text id="SvgjsText5873" font-family="inherit" x="191.3620748637635" y="229" text-anchor="middle" dominant-baseline="auto" font-size="12px" font-weight="600" fill="#373d3f" class="apexcharts-text apexcharts-xaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5874">Jul '20</tspan><title>Jul '20</title></text><text id="SvgjsText5876" font-family="inherit" x="325.31552726839794" y="229" text-anchor="middle" dominant-baseline="auto" font-size="12px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-xaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5877">08 Jul</tspan><title>08 Jul</title></text><text id="SvgjsText5879" font-family="inherit" x="478.40518715940874" y="229" text-anchor="middle" dominant-baseline="auto" font-size="12px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-xaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5880">16 Jul</tspan><title>16 Jul</title></text><text id="SvgjsText5882" font-family="inherit" x="631.4948470504198" y="229" text-anchor="middle" dominant-baseline="auto" font-size="12px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-xaxis-label " style="font-family: inherit;"><tspan id="SvgjsTspan5883">24 Jul</tspan><title>24 Jul</title></text></g></g><g id="SvgjsG5904" class="apexcharts-yaxis-annotations"></g><g id="SvgjsG5905" class="apexcharts-xaxis-annotations"></g><g id="SvgjsG5906" class="apexcharts-point-annotations"></g><rect id="SvgjsRect5907" width="0" height="0" x="0" y="0" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fefefe" class="apexcharts-zoom-rect"></rect><rect id="SvgjsRect5908" width="0" height="0" x="0" y="0" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fefefe" class="apexcharts-selection-rect"></rect></g></svg><div class="apexcharts-tooltip apexcharts-theme-dark" style="left: 593.315px; top: 20.8594px;"><div class="apexcharts-tooltip-title" style="font-family: inherit; font-size: 12px;">25 Jul</div><div class="apexcharts-tooltip-series-group apexcharts-tooltip-series-group-0 apexcharts-active" style="order: 1; display: flex;"><span class="apexcharts-tooltip-marker" style="background-color: color-mix(in srgb, transparent, var(--tblr-primary) 100%);"></span><div class="apexcharts-tooltip-text" style="font-family: inherit; font-size: 12px;"><div class="apexcharts-tooltip-y-group"><span class="apexcharts-tooltip-text-y-label">Web: </span><span class="apexcharts-tooltip-text-y-value">81</span></div><div class="apexcharts-tooltip-goals-group"><span class="apexcharts-tooltip-text-goals-label"></span><span class="apexcharts-tooltip-text-goals-value"></span></div><div class="apexcharts-tooltip-z-group"><span class="apexcharts-tooltip-text-z-label"></span><span class="apexcharts-tooltip-text-z-value"></span></div></div></div><div class="apexcharts-tooltip-series-group apexcharts-tooltip-series-group-1" style="order: 2; display: none;"><span class="apexcharts-tooltip-marker" style="background-color: color-mix(in srgb, transparent, var(--tblr-primary) 100%);"></span><div class="apexcharts-tooltip-text" style="font-family: inherit; font-size: 12px;"><div class="apexcharts-tooltip-y-group"><span class="apexcharts-tooltip-text-y-label">Web: </span><span class="apexcharts-tooltip-text-y-value">81</span></div><div class="apexcharts-tooltip-goals-group"><span class="apexcharts-tooltip-text-goals-label"></span><span class="apexcharts-tooltip-text-goals-value"></span></div><div class="apexcharts-tooltip-z-group"><span class="apexcharts-tooltip-text-z-label"></span><span class="apexcharts-tooltip-text-z-value"></span></div></div></div><div class="apexcharts-tooltip-series-group apexcharts-tooltip-series-group-2" style="order: 3; display: none;"><span class="apexcharts-tooltip-marker" style="background-color: color-mix(in srgb, transparent, var(--tblr-primary) 100%);"></span><div class="apexcharts-tooltip-text" style="font-family: inherit; font-size: 12px;"><div class="apexcharts-tooltip-y-group"><span class="apexcharts-tooltip-text-y-label">Web: </span><span class="apexcharts-tooltip-text-y-value">81</span></div><div class="apexcharts-tooltip-goals-group"><span class="apexcharts-tooltip-text-goals-label"></span><span class="apexcharts-tooltip-text-goals-value"></span></div><div class="apexcharts-tooltip-z-group"><span class="apexcharts-tooltip-text-z-label"></span><span class="apexcharts-tooltip-text-z-value"></span></div></div></div></div><div class="apexcharts-yaxistooltip apexcharts-yaxistooltip-0 apexcharts-yaxistooltip-left apexcharts-theme-dark"><div class="apexcharts-yaxistooltip-text"></div></div></div></div>
                  </div>
                </div>
              </div>






















<!--{% extends 'base.html' %}-->
{% load static %}
<!--{% block content %}-->



.navbar-text {
        color: #f0f0f0;
      }
      .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
      }
      h1, h2, h3, h4, h5, h6 {
        color: #f0f0f0;
      }
      /* MOBILE: disable sticky */
      @media (max-width: 767px) {
        .header-banner,
        .header-header {
          position: static !important;
        }

        body {
          padding-top: 0;
        }
      }



<div class="container-fluid px-md-5 px-3 mt-3">


  







  <!-- Welcome Section with Performance Message and Action Buttons -->
  <div class="row align-items-center mb-4">
    <!-- Performance Message and Badge -->
    <div class="col text-light">
      <div class="d-flex flex-column flex-md-row align-items-start align-items-md-center gap-3">
        <div class="flex-grow-1">
          <span class="badge {{ badge.class }}">
            <i class="bi bi-alarm-fill me-1 fs-1"></i>
            You have {{ entry_count }} entry{% if entry_count != 1 %}(s){% endif %} so far
          </span>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="col-auto d-flex gap-2">
      <a href="{% url 'create_guest' %}" class="btn btn-success d-flex align-items-center">
        <i class="bi bi-person-plus-fill me-1"></i> Add Guest
      </a>
      {% if is_admin_group or request.user.is_superuser %}
      <a href="{% url 'create_user' %}" class="btn btn-secondary d-flex align-items-center">
        <i class="bi-person-badge-fill"></i> Add User
      </a>
      {% endif %}
      <div class="dropdown ms-auto">
        <button class="btn btn-primary dropdown-toggle d-flex align-items-center" data-bs-toggle="dropdown">
          <i class="bi bi-share me-1"></i> Import/Export
        </button>
        <div class="dropdown-menu dropdown-menu-end p-2" style="min-width: 260px;">
          <!-- Download CSV Template -->
          <a href="{% url 'download_csv_template' %}" class="btn btn-outline-primary">
              <i class="ti ti-download"></i> Download CSV Template
          </a>

          <!-- Trigger Button -->
          <button type="button" class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#importCSVModal">
            <i class="bi bi-upload"></i> Import CSV
          </button>

          <!-- Export as CSV -->
          <a class="dropdown-item d-flex align-items-center" href="{% url 'export_csv' %}?{{ request.GET.urlencode }}">
            <i class="bi bi-filetype-csv me-2"></i> Export as CSV
          </a>

          <!-- Export as Excel -->
          <a class="dropdown-item d-flex align-items-center" href="{% url 'export_excel' %}?{{ request.GET.urlencode }}">
            <i class="bi bi-file-earmark-excel me-2 text-success"></i> Export as Excel
          </a>

          <hr class="dropdown-divider">

          <!-- Import from Excel -->
          <form method="post" action="{% url 'import_excel' %}" enctype="multipart/form-data" class="dropdown-item p-0">
            {% csrf_token %}
            <label class="form-label small text-muted ms-3 mt-2 mb-1">Import Excel</label>
            <div class="px-3">
              <input type="file" name="excel_file" class="form-control form-control-sm mb-2" accept=".xlsx,.xls">
              <button type="submit" class="btn btn-sm btn-outline-success w-100">
                <i class="bi bi-upload me-1"></i> Upload Excel
              </button>
            </div>
          </form>
        </div>
      </div>


    </div>
  </div>





  <!-- Guest Cards -->
  <div class="row">
    {% for guest in page_obj %}
    <div class="col-12 col-sm-6 col-md-4 col-lg-4 mb-4 d-flex">
      <div class="card position-relative overflow-visible bg-dark border-0 shadow-lg text-light w-100 h-100 d-flex flex-column"
          style="min-height: 270px; max-width: 100%; overflow: hidden; word-break: break-word; box-shadow: 0 0 10px rgba(0,0,0,0.3);">

        <div class="card-body p-3 d-flex gap-3 flex-grow-1">
          {% if guest.picture %}
            <img src="{{ guest.picture.url }}"
                alt="{{ guest.full_name }}"
                class="rounded shadow-sm border-0 flex-shrink-0"
                style="width: 100px; height: 100px; object-fit: cover;"
                data-bs-toggle="modal"
                data-bs-target="#previewModal{{ guest.id }}">
          {% else %}
            <img src="https://res.cloudinary.com/dahx6bbyr/image/upload/v1753468187/default_guest_memhgq.jpg"
                alt="{{ guest.full_name }}"
                class="rounded shadow-sm border-0 flex-shrink-0"
                style="width: 100px; height: 100px; object-fit: cover;"
                data-bs-toggle="modal"
                data-bs-target="#previewModal{{ guest.id }}">
          {% endif %}



          <div class="d-flex flex-column flex-grow-1" style="min-width: 0;">
            <h2 class="card-title mb-1 text-white fs-2 fw-bold" title="{{ guest.title }} {{ guest.full_name }}">
              {{ guest.title }} {{ guest.full_name }}
            </h2>

            <div class="text fs-3 small mb-2" title="{{ guest.phone_number }}">
              <a href="tel:{{ guest.phone_number }}" class="text-info text-decoration-none">{{ guest.phone_number }}</a>
            </div>

            <div class="text fs-4 small mb-2" style="word-break: break-word;" title="{{ guest.service_attended }}">
              <strong>Service Attended:</strong> {{ guest.service_attended }}
            </div>

            <!-- Status Dropdown -->
            <div class="dropdown dropup mb-2 mt-auto">
              <a href="#" class="dropdown-toggle text-uppercase fw-bold text-{{ guest.get_status_color }}" data-bs-toggle="dropdown" aria-expanded="false">
                {{ guest.status }}
                {% if guest.status == "Planted" %}
                  <i class="bi bi-star-fill ms-1"></i>
                {% elif guest.status == "Work in Progress" %}
                  <i class="bi bi-arrow-repeat ms-1"></i>
                {% elif guest.status == "Planted Elsewhere" %}
                  <i class="bi bi-x-octagon-fill ms-1"></i>
                {% else %}
                  <i class="bi bi-question-circle-fill ms-1"></i>
                {% endif %}
              </a>
              <div class="dropdown-menu">
                {% for key, label in guest.STATUS_CHOICES %}
                <a class="dropdown-item text-white" href="{% url 'update_status' guest.id key %}">
                  {{ label }}
                </a>
                {% endfor %}
              </div>
            </div>

            <!-- Assignment / Creator Badges -->
            {% if is_staff_group or request.user.is_superuser %}
              {% if guest.assigned_to and guest.assigned_to != guest.created_by %}
                <span class="badge bg-grey text-warning">
                  Assigned to: {{ guest.assigned_to.get_full_name|default:guest.assigned_to.username }}
                </span>
                <span class="badge bg-grey text-success">
                  Created by: {{ guest.created_by.get_full_name|default:guest.created_by.username }}
                </span>
              {% else %}
                <span class="badge bg-grey text-success">
                  Created by: {{ guest.created_by.get_full_name|default:guest.created_by.username }}
                </span>
              {% endif %}
            {% else %}
              {% if guest.assigned_to and guest.assigned_to != guest.created_by %}
                <span class="badge bg-grey text-danger">
                  Assigned to you
                </span>
              {% endif %}
            {% endif %}

            {% if is_staff_group or request.user.is_superuser %}
              <form method="post" action="{% url 'reassign_guest' guest.id %}" class="d-flex mt-2" style="gap: 0.5rem;">
                {% csrf_token %}
                <select name="assigned_to" class="form-select form-select-sm">
                  <option value="">-- Assign to user --</option>
                  {% for u in users %}
                    <option value="{{ u.id }}" {% if guest.assigned_to == u %}selected{% endif %}>
                      {{ u.get_full_name|default:u.username }}
                    </option>
                  {% endfor %}
                </select>
                <button type="submit" class="btn btn-sm btn-outline-primary">Reassign</button>
              </form>
            {% endif %}


            <!-- Actions -->
            <div class="mt-2">
              <a href="{% url 'edit_guest' guest.id %}" class="btn btn-sm btn-warning">
                <i class="ti ti-edit"></i> Edit
              </a>

              <!-- Follow-Up Report Icon/Button -->
              <button 
                class="btn btn-sm btn-outline-info"
                data-bs-toggle="modal"
                data-bs-target="#followupModal"
                data-guest-id="{{ guest.id }}"
                title="Add Follow-Up Report"
              >
                <i class="bi bi-info fs-4"></i> Report {{ guest.report_count }}
              </button>

              <!-- Last Reported -->
              <div class="text-sm mt-2">
                <strong>Last Reported:</strong>
                {% if guest.last_reported %}
                  {{ guest.last_reported|date:"M d, Y" }}
                {% else %}
                  Never
                {% endif %}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    {% empty %}
      <div class="col text-center text-muted">No guest entries found.</div>
    {% endfor %}
  </div>

  {% if page_obj.has_other_pages %}
  <nav aria-label="Page navigation">
    <ul class="pagination justify-content-center flex-wrap">

      <!-- Previous Page -->
      {% if page_obj.has_previous %}
        <li class="page-item">
          <a class="page-link" href="?page={{ page_obj.previous_page_number }}" aria-label="Previous">&laquo;</a>
        </li>
      {% else %}
        <li class="page-item disabled"><span class="page-link">&laquo;</span></li>
      {% endif %}

      <!-- Page Numbers with Ellipses -->
      {% for i in page_obj.paginator.page_range %}
        {% if i == 1 or i == page_obj.paginator.num_pages or i >= page_obj.number|add:'-1' and i <= page_obj.number|add:'1' %}
          {% if i == page_obj.number %}
            <li class="page-item active"><span class="page-link">{{ i }}</span></li>
          {% else %}
            <li class="page-item"><a class="page-link" href="?page={{ i }}">{{ i }}</a></li>
          {% endif %}
        {% elif i == page_obj.number|add:'-2' or i == page_obj.number|add:'2' %}
          <li class="page-item disabled"><span class="page-link">…</span></li>
        {% endif %}
      {% endfor %}

      <!-- Next Page -->
      {% if page_obj.has_next %}
        <li class="page-item">
          <a class="page-link" href="?page={{ page_obj.next_page_number }}" aria-label="Next">&raquo;</a>
        </li>
      {% else %}
        <li class="page-item disabled"><span class="page-link">&raquo;</span></li>
      {% endif %}

    </ul>
  </nav>
  {% endif %}

  {% for guest in page_obj %}
  <div class="modal fade" id="previewModal{{ guest.id }}" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark border-light text-white">
        <div class="modal-body text-center">
          <img src="{% if guest.picture %}{{ guest.picture.url }}{% else %}{{ MEDIA_URL }}guest_pictures/default_guest.jpg{% endif %}"
              class="img-fluid rounded shadow">
          <p class="mt-3 mb-0 fw-bold">{{ guest.full_name }}</p>
        </div>
      </div>
    </div>
  </div>
  {% endfor %}


  









<div class="sticky-top">
  <header class="navbar navbar-expand-md sticky-top d-print-none">
    <div class="container-xl">
      <!-- BEGIN NAVBAR TOGGLER -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-menu" aria-controls="navbar-menu" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <!-- END NAVBAR TOGGLER -->
      <!-- BEGIN NAVBAR LOGO -->
      <div class="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
        <a href="/" class="navbar-brand d-flex align-items-center">
          <img src="{% static 'images/church_logo.png' %}" alt="Logo" width="80" height="80" class="me-2">
          <span class="text-white fw-bold"></span>
        </a>
      </div>
      <!-- END NAVBAR LOGO -->
      <div class="navbar-nav flex-row order-md-last">
        <div class="nav-item d-none d-md-flex me-3">
          <div class="btn-list">
            <a href="https://gatewaynation.org" class="btn btn-5" target="_blank" rel="noreferrer">
              <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-world-www">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M19.5 7a9 9 0 0 0 -7.5 -4a8.991 8.991 0 0 0 -7.484 4" />
                <path d="M11.5 3a16.989 16.989 0 0 0 -1.826 4" /><path d="M12.5 3a16.989 16.989 0 0 1 1.828 4" />
                <path d="M19.5 17a9 9 0 0 1 -7.5 4a8.991 8.991 0 0 1 -7.484 -4" /><path d="M11.5 21a16.989 16.989 0 0 1 -1.826 -4" />
                <path d="M12.5 21a16.989 16.989 0 0 0 1.828 -4" /><path d="M2 10l1 4l1.5 -4l1.5 4l1 -4" /><path d="M17 10l1 4l1.5 -4l1.5 4l1 -4" /><path d="M9.5 10l1 4l1.5 -4l1.5 4l1 -4" />
              </svg>
              Gateway Nation
            </a>
          </div>
        </div>
        <div class="d-none d-md-flex">
          <div class="nav-item">
            <a href="?theme=dark" class="nav-link px-0 hide-theme-dark" data-bs-toggle="tooltip" data-bs-placement="bottom" aria-label="Enable dark mode" data-bs-original-title="Enable dark mode">
              <!-- Download SVG icon from http://tabler.io/icons/icon/moon -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z"></path>
              </svg>
            </a>
            <a href="?theme=light" class="nav-link px-0 hide-theme-light" data-bs-toggle="tooltip" data-bs-placement="bottom" aria-label="Enable light mode" data-bs-original-title="Enable light mode">
              <!-- Download SVG icon from http://tabler.io/icons/icon/sun -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                <path d="M12 12m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"></path>
                <path d="M3 12h1m8 -9v1m8 8h1m-9 8v1m-6.4 -15.4l.7 .7m12.1 -.7l-.7 .7m0 11.4l.7 .7m-12.1 -.7l-.7 .7"></path>
              </svg>
            </a>
          </div>
          <div class="nav-item dropdown d-none d-md-flex">
            <a href="#" class="nav-link px-0" data-bs-toggle="dropdown" tabindex="-1" aria-label="Show notifications" data-bs-auto-close="outside" aria-expanded="false">
              <!-- Download SVG icon from http://tabler.io/icons/icon/bell -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                <path d="M10 5a2 2 0 1 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6"></path>
                <path d="M9 17v1a3 3 0 0 0 6 0v-1"></path>
              </svg>
              <span class="badge bg-red"></span>
            </a>
            <div class="dropdown-menu dropdown-menu-arrow dropdown-menu-end dropdown-menu-card">
              <div class="card">
                <div class="card-header d-flex">
                  <h3 class="card-title">Notifications</h3>
                  <div class="btn-close ms-auto" data-bs-dismiss="dropdown"></div>
                </div>
                <div class="list-group list-group-flush list-group-hoverable">
                  <div class="list-group-item">
                    <div class="row align-items-center">
                      <div class="col-auto"><span class="status-dot status-dot-animated bg-red d-block"></span></div>
                      <div class="col text-truncate">
                        <a href="#" class="text-body d-block">Example 1</a>
                        <div class="d-block text-secondary text-truncate mt-n1">Change deprecated html tags to text decoration classes (#29604)</div>
                      </div>
                      <div class="col-auto">
                        <a href="#" class="list-group-item-actions">
                          <!-- Download SVG icon from http://tabler.io/icons/icon/star -->
                          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon text-muted icon-2">
                            <path d="M12 17.75l-6.172 3.245l1.179 -6.873l-5 -4.867l6.9 -1l3.086 -6.253l3.086 6.253l6.9 1l-5 4.867l1.179 6.873z"></path>
                          </svg>
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="card-body">
                  <div class="row">
                    <div class="col">
                      <a href="#" class="btn btn-2 w-100"> Archive all </a>
                    </div>
                    <div class="col">
                      <a href="#" class="btn btn-2 w-100"> Mark all as read </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="nav-item dropdown d-none d-md-flex me-3">
            <a href="#" class="nav-link px-0" data-bs-toggle="dropdown" tabindex="-1" aria-label="Show app menu" data-bs-auto-close="outside" aria-expanded="false">
              <!-- Download SVG icon from http://tabler.io/icons/icon/apps -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                <path d="M4 4m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"></path>
                <path d="M4 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"></path>
                <path d="M14 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"></path>
                <path d="M14 7l6 0"></path>
                <path d="M17 4l0 6"></path>
              </svg>
            </a>
            <div class="dropdown-menu dropdown-menu-arrow dropdown-menu-end dropdown-menu-card">
              <div class="card">
                <div class="card-header">
                  <div class="card-title">My Apps</div>
                  <div class="card-actions btn-actions">
                    <a href="#" class="btn-action">
                      <!-- Download SVG icon from http://tabler.io/icons/icon/settings -->
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                        <path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z"></path>
                        <path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"></path>
                      </svg>
                    </a>
                  </div>
                </div>
                <div class="card-body scroll-y p-2" style="max-height: 50vh">
                  <div class="row g-0">
                    <div class="col-4">
                      <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                        <img src="./static/brands/google-analytics.svg" class="w-6 h-6 mx-auto mb-2" width="24" height="24" alt="">
                        <span class="h5">Google Analytics</span>
                      </a>
                    </div>
                    <div class="col-4">
                      <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                        <img src="./static/brands/google-drive.svg" class="w-6 h-6 mx-auto mb-2" width="24" height="24" alt="">
                        <span class="h5">Google Drive</span>
                      </a>
                    </div>
                    <div class="col-4">
                      <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                        <img src="./static/brands/google-meet.svg" class="w-6 h-6 mx-auto mb-2" width="24" height="24" alt="">
                        <span class="h5">Google Meet</span>
                      </a>
                    </div>
                    <div class="col-4">
                      <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                        <img src="./static/brands/google-photos.svg" class="w-6 h-6 mx-auto mb-2" width="24" height="24" alt="">
                        <span class="h5">Google Photos</span>
                      </a>
                    </div>
                    <div class="col-4">
                      <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                        <img src="./static/brands/google-teams.svg" class="w-6 h-6 mx-auto mb-2" width="24" height="24" alt="">
                        <span class="h5">Google Teams</span>
                      </a>
                    </div>                          
                    <div class="col-4">
                      <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                        <img src="./static/brands/whatsapp.svg" class="w-6 h-6 mx-auto mb-2" width="24" height="24" alt="">
                        <span class="h5">WhatsApp</span>
                      </a>
                    </div>
                    <div class="col-4">
                      <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                        <img src="./static/brands/zoom.svg" class="w-6 h-6 mx-auto mb-2" width="24" height="24" alt="">
                        <span class="h5">Zoom</span>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="nav-item dropdown">
          <a href="#" class="nav-link d-flex lh-1 p-0 px-2" data-bs-toggle="dropdown" aria-label="Open user menu">
            <span class="avatar avatar-sm" style="background-image: url(./static/avatars/000m.jpg)"> </span>
            <div class="d-none d-xl-block ps-2">
              <div>Paweł Kuna</div>
              <div class="mt-1 small text-secondary">UI Designer</div>
            </div>
          </a>
          <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
            <a href="#" class="dropdown-item">Status</a>
            <a href="./profile.html" class="dropdown-item">Profile</a>
            <a href="#" class="dropdown-item">Feedback</a>
            <div class="dropdown-divider"></div>
            <a href="./settings.html" class="dropdown-item">Settings</a>
            <a href="./sign-in.html" class="dropdown-item">Logout</a>
          </div>
        </div>
      </div>
    </div>
  </header>
  <header class="navbar-expand-md">
    <div class="collapse navbar-collapse" id="navbar-menu">
      <div class="navbar">
        <div class="container-xl">
          <div class="row flex-column flex-md-row flex-fill align-items-center">
            <div class="col">
              <!-- BEGIN NAVBAR MENU -->
              <ul class="navbar-nav">
                <li class="nav-item">
                  <a class="nav-link" href="./">
                    <span class="nav-link-icon d-md-none d-lg-inline-block"><!-- Download SVG icon from http://tabler.io/icons/icon/home -->
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                        <path d="M5 12l-2 0l9 -9l9 9l-2 0"></path>
                        <path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7"></path>
                        <path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6"></path></svg></span>
                    <span class="nav-link-title"> Dashboard </span>
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="./">
                    <span class="nav-link-icon d-md-none d-lg-inline-block"><!-- Download SVG icon from http://tabler.io/icons/icon/home -->
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                        <path d="M5 12l-2 0l9 -9l9 9l-2 0"></path>
                        <path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7"></path>
                        <path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6"></path></svg></span>
                    <span class="nav-link-title"> Guests </span>
                  </a>
                </li>
              </ul>
              <!-- END NAVBAR MENU -->
            </div>
            <div class="col col-md-auto">
              <ul class="navbar-nav">
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#navbar-base" data-bs-toggle="dropdown" data-bs-auto-close="outside" role="button" aria-expanded="false">
                    <span class="nav-link-icon d-md-none d-lg-inline-block"><!-- Download SVG icon from http://tabler.io/icons/icon/package -->
                      <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="currentColor"  class="icon icon-tabler icons-tabler-filled icon-tabler-filters">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M19.396 11.056a6 6 0 0 1 -5.647 10.506q .206 -.21 .396 -.44a8 8 0 0 0 1.789 -6.155a8.02 8.02 0 0 0 3.462 -3.911" />
                        <path d="M4.609 11.051a7.99 7.99 0 0 0 9.386 4.698a6 6 0 1 1 -9.534 -4.594z" /><path d="M12 2a6 6 0 1 1 -6 6l.004 -.225a6 6 0 0 1 5.996 -5.775" />
                      </svg>
                    </span>
                    <span class="nav-link-title"> Filters </span>
                  </a>
                  <div class="dropdown-menu">
                    <div class="dropend">
                      <a class="dropdown-item dropdown-toggle" href="#sidebar-authentication" data-bs-toggle="dropdown" data-bs-auto-close="outside" role="button" aria-expanded="false">
                        Authentication
                      </a>
                      <div class="dropdown-menu">
                        <a href="./sign-in.html" class="dropdown-item"> Sign in </a>
                        <a href="./sign-in-link.html" class="dropdown-item"> Sign in link </a>
                      </div>
                    </div>
                  </div>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#" data-bs-toggle="offcanvas" data-bs-target="#offcanvasSettings">
                    <span class="badge badge-sm bg-red text-red-fg">New</span>
                    <span class="nav-link-icon d-md-none d-lg-inline-block">
                      <!-- Download SVG icon from http://tabler.io/icons/icon/settings -->
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                        <path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z"></path>
                        <path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"></path>
                      </svg>
                    </span>
                    <span class="nav-link-title"> Theme Settings </span>
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</div>
    

<div class="page-wrapper">

  <!-- Page Header -->
  <div class="page-header d-print-none" aria-label="Page header">
    <div class="container-xl">
      <div class="row g-2 align-items-center">
        <div class="col">
          <h2 class="page-title">Overview</h2>
        </div>
        <div class="col-auto ms-auto d-print-none">
          <div class="btn-list">
            <span class="d-none d-sm-inline">
              <a href="{% url 'guest_list' %}" class="btn btn-warning btn-1"> Guests </a>
            </span>
            <div class="dropdown">
              <button class="btn btn-primary dropdown-toggle d-flex align-items-center" data-bs-toggle="dropdown">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-2">
                  <path d="M12 5l0 14"></path>
                  <path d="M5 12l14 0"></path>
                </svg>
                Records
              </button>
              <a href="#" class="btn btn-primary btn-6 d-sm-none btn-icon" data-bs-toggle="modal" data-bs-target="#modal-report" aria-label="Create new report">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-2">
                  <path d="M12 5l0 14"></path>
                  <path d="M5 12l14 0"></path>
                </svg>
              </a>
              <div class="dropdown-menu shadow-sm" style="min-width: 100px;">
                <div class="col-auto flex-column d-flex gap-2">
                  <a href="{% url 'create_guest' %}" class="btn btn-success d-flex align-items-center">
                    <i class="bi bi-person-plus-fill me-1"></i> Add Guest
                  </a>
                  {% if is_admin_group or request.user.is_superuser %}
                  <a href="{% url 'create_user' %}" class="btn btn-secondary d-flex align-items-center">
                    <i class="bi bi-person-badge-fill me-1"></i> Add User
                  </a>
                  {% endif %}
                  <button class="btn bg-dark shadow-lg d-flex flex-wrap gap-2 align-items-center justify-content-end" data-chart="myChart">
                    <i class="ti ti-photo"></i> Export PNG
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>


  



  <!-- Page Body -->
  <div class="page-body">
    <div class="container-xl">
      <div class="row row-deck g-4">

        <div class="row mb-4">
          <div class="col-auto">
            <select id="dashboardYearSelect" class="form-select form-select-sm">
              <option>Loading years...</option>
            </select>
          </div>
          <div class="col-auto">
            <select id="dashboardMonthSelect" class="form-select form-select-sm">
              <option value="">All Months</option>
            </select>
          </div>
        </div>

        <!-- Row 1: Welcome + Total Guests -->
        <div class="col-sm-12 col-lg-6">
          <div class="card">
            <div class="card-body">
              <div class="row gy-3">

                <!-- Welcome Message -->
                <div class="col-12 col-sm d-flex flex-column">
                  <h1 class="h2">Welcome back, {{ request.user.get_full_name }}</h1>
                    

                  <!-- Stats Row -->
                  <div class="row g-5 mt-auto">

                    <!-- User's Guest Count -->
                    <div class="col-auto">
                      <div class="subheader">My Guests</div>
                      <div class="d-flex align-items-baseline">
                        <div class="h3 me-2">
                          {{ planted_guest_count }}
                        </div>
                        <div class="me-auto">
                          <span class="text-green d-inline-flex align-items-center lh-1">
                            +{{ planted_percent_change }}%
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="icon ms-1 icon-2">
                              <path d="M3 17l6 -6l4 4l8 -8"></path>
                              <path d="M14 7h7v7"></path>
                            </svg>
                          </span>
                        </div>
                      </div>
                      <div class="progress progress-sm">
                        <div class="progress-bar bg-success" style="width: {{ planted_percent_change }}%" 
                            role="progressbar" aria-valuenow="{{ planted_percent_change }}" 
                            aria-valuemin="0" aria-valuemax="100">
                          <span class="visually-hidden">{{ planted_percent_change }}% Complete</span>
                        </div>
                      </div>
                    </div>

                    <!-- Church Guest Count -->
                    <div class="col-auto">
                      <div class="subheader">Total Church Guests</div>
                      <div class="d-flex align-items-baseline">
                        <div class="h3 me-2">
                          {{ planted_guest_count }}
                        </div>
                        <div class="me-auto">
                          <span class="text-green d-inline-flex align-items-center lh-1">
                            +{{ planted_percent_change }}%
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                class="icon ms-1 icon-2">
                              <path d="M3 17l6 -6l4 4l8 -8"></path>
                              <path d="M14 7h7v7"></path>
                            </svg>
                          </span>
                        </div>
                      </div>
                      <div class="progress progress-sm">
                        <div class="progress-bar bg-success" style="width: {{ planted_percent_change }}%" 
                            role="progressbar" aria-valuenow="{{ planted_percent_change }}" 
                            aria-valuemin="0" aria-valuemax="100">
                          <span class="visually-hidden">{{ planted_percent_change }}% Complete</span>
                        </div>
                      </div>
                    </div>

                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-sm-6 col-lg-3">
          <div class="card">
            <div class="card-body">
              
              <!-- Header -->
              <div class="subheader">Total Guests</div>

              <!-- Total + Percent Change -->
              <div class="d-flex align-items-baseline">
                <div class="h1 mb-0 me-2">
                  {{ total_guests }}
                </div>
                <div class="me-auto">
                  <span class="text-green d-inline-flex align-items-center lh-1">
                    {{ percent_change }}%
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                        viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="icon ms-1 icon-2">
                      <path d="M3 17l6 -6l4 4l8 -8"></path>
                      <path d="M14 7l7 0l0 7"></path>
                    </svg>
                  </span>
                </div>
              </div>

              <!-- Subtext -->
              <div class="text-secondary mt-2">
                {{ monthly_increase }} guests added this month
              </div>
            </div>

            <!-- Chart Placeholder -->
            <div id="chart-visitors" class="position-relative" style="min-height: 96px;">
              <!-- ApexCharts will inject a mini line chart here -->
            </div>
          </div>
        </div>


        <div class="col-sm-6 col-lg-3">
                <div class="card">
                  <div class="card-body">
                    <div class="subheader">Most Attended Service</div>
                    <div class="d-flex align-items-baseline mb-2">
                      <div class="h1 mb-0 me-2">25,782</div>
                      <div class="me-auto">
                        <span class="text-red d-inline-flex align-items-center lh-1">
                          -1%
                          <!-- Download SVG icon from http://tabler.io/icons/icon/trending-down -->
                          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon ms-1 icon-2">
                            <path d="M3 7l6 6l4 -4l8 8"></path>
                            <path d="M21 10l0 7l-7 0"></path>
                          </svg>
                        </span>
                      </div>
                    </div>
                    <div id="chart-active-users-3" class="position-relative" style="min-height: 130px;"><div id="apexchartsmlkcvvnu" class="apexcharts-canvas apexchartsmlkcvvnu apexcharts-theme-" style="width: 344px; height: 130px;"><svg id="SvgjsSvg3453" width="344" height="130" xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.dev" class="apexcharts-svg" xmlns:data="ApexChartsNS" transform="translate(0, 0)"><foreignObject x="0" y="0" width="344" height="130"><div class="apexcharts-legend" xmlns="http://www.w3.org/1999/xhtml"></div><style type="text/css">
      .apexcharts-flip-y {
        transform: scaleY(-1) translateY(-100%);
        transform-origin: top;
        transform-box: fill-box;
      }
      .apexcharts-flip-x {
        transform: scaleX(-1);
        transform-origin: center;
        transform-box: fill-box;
      }
      .apexcharts-legend {
        display: flex;
        overflow: auto;
        padding: 0 10px;
      }
      .apexcharts-legend.apx-legend-position-bottom, .apexcharts-legend.apx-legend-position-top {
        flex-wrap: wrap
      }
      .apexcharts-legend.apx-legend-position-right, .apexcharts-legend.apx-legend-position-left {
        flex-direction: column;
        bottom: 0;
      }
      .apexcharts-legend.apx-legend-position-bottom.apexcharts-align-left, .apexcharts-legend.apx-legend-position-top.apexcharts-align-left, .apexcharts-legend.apx-legend-position-right, .apexcharts-legend.apx-legend-position-left {
        justify-content: flex-start;
      }
      .apexcharts-legend.apx-legend-position-bottom.apexcharts-align-center, .apexcharts-legend.apx-legend-position-top.apexcharts-align-center {
        justify-content: center;
      }
      .apexcharts-legend.apx-legend-position-bottom.apexcharts-align-right, .apexcharts-legend.apx-legend-position-top.apexcharts-align-right {
        justify-content: flex-end;
      }
      .apexcharts-legend-series {
        cursor: pointer;
        line-height: normal;
        display: flex;
        align-items: center;
      }
      .apexcharts-legend-text {
        position: relative;
        font-size: 14px;
      }
      .apexcharts-legend-text *, .apexcharts-legend-marker * {
        pointer-events: none;
      }
      .apexcharts-legend-marker {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        margin-right: 1px;
      }

      .apexcharts-legend-series.apexcharts-no-click {
        cursor: auto;
      }
      .apexcharts-legend .apexcharts-hidden-zero-series, .apexcharts-legend .apexcharts-hidden-null-series {
        display: none !important;
      }
      .apexcharts-inactive-legend {
        opacity: 0.45;
      }</style></foreignObject><g id="SvgjsG3455" class="apexcharts-inner apexcharts-graphical" transform="translate(76, 1)"><defs id="SvgjsDefs3454"><clipPath id="gridRectMaskmlkcvvnu"><rect id="SvgjsRect3456" width="192" height="190" x="0" y="0" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fff"></rect></clipPath><clipPath id="gridRectBarMaskmlkcvvnu"><rect id="SvgjsRect3457" width="198" height="196" x="-3" y="-3" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fff"></rect></clipPath><clipPath id="gridRectMarkerMaskmlkcvvnu"><rect id="SvgjsRect3458" width="192" height="190" x="0" y="0" rx="0" ry="0" opacity="1" stroke-width="0" stroke="none" stroke-dasharray="0" fill="#fff"></rect></clipPath><clipPath id="forecastMaskmlkcvvnu"></clipPath><clipPath id="nonForecastMaskmlkcvvnu"></clipPath></defs><g id="SvgjsG3461" class="apexcharts-radialbar"><g id="SvgjsG3462"><g id="SvgjsG3463" class="apexcharts-tracks"><g id="SvgjsG3464" class="apexcharts-radialbar-track apexcharts-track" rel="1"><path id="apexcharts-radialbarTrack-0" d="M 43.6688307835135 125.21341463414635 A 60.42682926829268 60.42682926829268 0 1 1 148.3311692164865 125.21341463414633 " fill="none" fill-opacity="1" stroke="rgba(242,242,242,0.85)" stroke-opacity="1" stroke-linecap="butt" stroke-width="17.625609756097564" stroke-dasharray="0" class="apexcharts-radialbar-area" data:pathOrig="M 43.6688307835135 125.21341463414635 A 60.42682926829268 60.42682926829268 0 1 1 148.3311692164865 125.21341463414633 "></path></g></g><g id="SvgjsG3466"><g id="SvgjsG3470" class="apexcharts-series apexcharts-radial-series" seriesName="" rel="1" data:realIndex="0"><path id="SvgjsPath3471" d="M 43.6688307835135 125.21341463414635 A 60.42682926829268 60.42682926829268 0 1 1 151.62318962020538 71.38935680897133 " fill="none" fill-opacity="0.85" stroke="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" stroke-opacity="1" stroke-linecap="butt" stroke-width="18.170731707317074" stroke-dasharray="0" class="apexcharts-radialbar-area apexcharts-radialbar-slice-0" data:angle="187" data:value="78" index="0" j="0" data:pathOrig="M 43.6688307835135 125.21341463414635 A 60.42682926829268 60.42682926829268 0 1 1 151.62318962020538 71.38935680897133 "></path></g><circle id="SvgjsCircle3467" r="35.6140243902439" cx="96" cy="95" class="apexcharts-radialbar-hollow" fill="transparent"></circle></g></g><g id="SvgjsG3459" class="apexcharts-datalabels-group" transform="translate(0, 0) scale(1)" style="opacity: 1;"><text id="SvgjsText4176" font-family="inherit" x="96" y="95" text-anchor="middle" dominant-baseline="auto" font-size="16px" font-weight="600" fill="color-mix(in srgb, transparent, var(--tblr-primary) 100%)" class="apexcharts-text apexcharts-datalabel-label" style="font-family: inherit;"></text><text id="SvgjsText4177" font-family="inherit" x="96" y="103" text-anchor="middle" dominant-baseline="auto" font-size="24px" font-weight="400" fill="#373d3f" class="apexcharts-text apexcharts-datalabel-value" style="font-family: inherit;">78%</text></g></g><line id="SvgjsLine3472" x1="0" y1="0" x2="192" y2="0" stroke="#b6b6b6" stroke-dasharray="0" stroke-width="1" stroke-linecap="butt" class="apexcharts-ycrosshairs"></line><line id="SvgjsLine3473" x1="0" y1="0" x2="192" y2="0" stroke-dasharray="0" stroke-width="0" stroke-linecap="butt" class="apexcharts-ycrosshairs-hidden"></line></g><g id="SvgjsG3460" class="apexcharts-datalabels-group" transform="translate(0, 0) scale(1)"></g></svg></div></div>
                  </div>
                </div>
              </div>


        <!-- Spacing -->
        <div class="w-100 my-3"></div>

        <!-- Row 2: Monthly Entry Chart -->
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Guest Entry Trend</h3>
            </div>
            <div class="card-body">
              <div id="chart-guest-entry" class="chart-lg" style="min-height: 240px;"></div>
            </div>
          </div>
        </div>


        <!-- Spacing -->
        <div class="w-100 my-3"></div>

        <!-- Row 3: Guest Status Cards -->
        <div class="col-14">
          <div class="row row-cols-1 row-cols-sm-2 row-cols-md-4 g-4">
            <div class="col d-flex">
              <div class="card card-sm h-100">
                <div class="card-body">
                  <div class="row align-items-center">
                    <!-- Icon Avatar -->
                    <div class="col-auto">
                      <span class="avatar bg-green text-white">
                        <!-- Icon: Check Copy (Filled) -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                            viewBox="0 0 24 24" fill="currentColor"
                            class="icon icon-tabler icons-tabler-filled icon-tabler-copy-check">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                          <path d="M18.333 6a3.667 3.667 0 0 1 3.667 3.667v8.666a3.667 3.667 0 0 1 -3.667 3.667h-8.666a3.667 3.667 0 0 1 -3.667 -3.667v-8.666a3.667 3.667 0 0 1 3.667 -3.667zm-3.333 -4c1.094 0 1.828 .533 2.374 1.514a1 1 0 1 1 -1.748 .972c-.221 -.398 -.342 -.486 -.626 -.486h-10c-.548 0 -1 .452 -1 1v9.998c0 .32 .154 .618 .407 .805l.1 .065a1 1 0 1 1 -.99 1.738a3 3 0 0 1 -1.517 -2.606v-10c0 -1.652 1.348 -3 3 -3zm1.293 9.293l-3.293 3.292l-1.293 -1.292a1 1 0 0 0 -1.414 1.414l2 2a1 1 0 0 0 1.414 0l4 -4a1 1 0 0 0 -1.414 -1.414" />
                        </svg>
                      </span>
                    </div>
                    <!-- Status Label & Count -->
                    <div class="col">
                      <div class="font-weight-medium">Planted</div>
                      <div class="text-secondary">
                        {{ planted_count }} guests
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col d-flex">
              <div class="card card-sm h-100">
                <div class="card-body">
                  <div class="row align-items-center">
                    <!-- Icon Avatar -->
                    <div class="col-auto">
                      <span class="avatar bg-danger text-white">
                        <!-- Icon: Copy X (Filled) -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                            viewBox="0 0 24 24" fill="currentColor"
                            class="icon icon-tabler icons-tabler-filled icon-tabler-copy-x">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                          <path d="M18.333 6a3.667 3.667 0 0 1 3.667 3.667v8.666a3.667 3.667 0 0 1 -3.667 3.667h-8.666a3.667 3.667 0 0 1 -3.667 -3.667v-8.666a3.667 3.667 0 0 1 3.667 -3.667zm-3.333 -4c1.094 0 1.828 .533 2.374 1.514a1 1 0 1 1 -1.748 .972c-.221 -.398 -.342 -.486 -.626 -.486h-10c-.548 0 -1 .452 -1 1v9.998c0 .32 .154 .618 .407 .805l.1 .065a1 1 0 1 1 -.99 1.738a3 3 0 0 1 -1.517 -2.606v-10c0 -1.652 1.348 -3 3 -3zm.8 8.786l-1.837 1.799l-1.749 -1.785a1 1 0 0 0 -1.319 -.096l-.095 .082a1 1 0 0 0 -.014 1.414l1.749 1.785l-1.835 1.8a1 1 0 0 0 -.096 1.32l.082 .095a1 1 0 0 0 1.414 .014l1.836 -1.8l1.75 1.786a1 1 0 0 0 1.319 .096l.095 -.082a1 1 0 0 0 .014 -1.414l-1.75 -1.786l1.836 -1.8a1 1 0 0 0 .096 -1.319l-.082 -.095a1 1 0 0 0 -1.414 -.014" />
                        </svg>
                      </span>
                    </div>
                    <!-- Status Label & Count -->
                    <div class="col">
                      <div class="font-weight-medium">Planted Elsewhere</div>
                      <div class="text-secondary">
                        {{ planted_elsewhere_count }} guests
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col d-flex">
              <div class="card card-sm h-100">
                <div class="card-body">
                  <div class="row align-items-center"> 
                    <!-- Icon Avatar -->
                    <div class="col-auto">
                      <span class="avatar bg-primary text-white">
                        <!-- Icon: Plane Departure -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                            viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="icon icon-tabler icons-tabler-outline icon-tabler-plane-departure">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                          <path d="M14.639 10.258l4.83 -1.294a2 2 0 1 1 1.035 3.863l-14.489 3.883l-4.45 -5.02l2.897 -.776l2.45 1.414l2.897 -.776l-3.743 -6.244l2.898 -.777l5.675 5.727z" />
                          <path d="M3 21h18" />
                        </svg>
                      </span>
                    </div>
                    <!-- Status Label & Count -->
                    <div class="col">
                      <div class="font-weight-medium">Relocated</div>
                      <div class="text-secondary">
                        {{ relocated_count }} guests
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col d-flex">
              <div class="card card-sm h-100">
                <div class="card-body">
                  <div class="row align-items-center">  
                    <!-- Icon Avatar -->
                    <div class="col-auto">
                      <span class="avatar bg-warning text-white">
                        <!-- Icon: Loader -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                            viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="icon icon-tabler icons-tabler-outline icon-tabler-loader">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                          <path d="M12 6l0 -3" />
                          <path d="M16.25 7.75l2.15 -2.15" />
                          <path d="M18 12l3 0" />
                          <path d="M16.25 16.25l2.15 2.15" />
                          <path d="M12 18l0 3" />
                          <path d="M7.75 16.25l-2.15 2.15" />
                          <path d="M6 12l-3 0" />
                          <path d="M7.75 7.75l-2.15 -2.15" />
                        </svg>
                      </span>
                    </div>
                    <!-- Status Label & Count -->
                    <div class="col">
                      <div class="font-weight-medium">Work in Progress</div>
                      <div class="text-secondary">
                        {{ work_in_progress_count }} guests
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Spacing -->
        <div class="w-100 my-3"></div>

        <!-- Row 4: Channel of Visit Chart -->
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Channel of Visit</h3>
            </div>
            <table class="table card-table table-vcenter">
              <thead>
                <tr>
                  <th>Channel</th>
                  <th>Guests</th>
                  <th class="w-50">Progress</th>
                </tr>
              </thead>
              <tbody id="channelProgressTableBody">
                {% for channel in channel_stats %}
                <tr>
                  <td>{{ channel.channel }}</td>
                  <td>{{ channel.count }}</td>
                  <td class="w-50">
                    <div class="progress progress-xs">
                      <div class="progress-bar bg-primary" style="width: {{ channel.percent }}%">
                      </div>
                    </div>
                  </td>
                </tr>
                {% empty %}
                <tr>
                  <td colspan="3" class="text-center text-muted">No data available</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </div>


        <!-- Spacing -->
        <div class="w-100 my-3"></div>

        <!-- Row 5: Service Attended Chart -->
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Service Attended</h3>
            </div>
            <div class="card-body">
              <div id="services-attended-chart" class="chart-lg" style="min-height: 300px;"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>



{% block extra_js %}
<script>
const monthNames = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

function loadYearsAndCurrent(yearSelectId, callback) {
  return fetch("/guests/api/guest-years/")
    .then(res => res.json())
    .then(data => {
      const yearSelect = document.getElementById(yearSelectId);
      yearSelect.innerHTML = data.years.map(y => `<option value="${y}">${y}</option>`).join('');
      yearSelect.value = data.current_year;
      if (callback) callback(data.current_year, data.current_month);
    });
}

function loadMonths(monthSelectId, year, defaultMonth = "") {
  return fetch(`/guests/api/guest-months/?year=${year}`)
    .then(res => res.json())
    .then(data => {
      const monthSelect = document.getElementById(monthSelectId);
      monthSelect.innerHTML = `<option value="">All Months</option>`;
      data.months.forEach(m => {
        monthSelect.innerHTML += `<option value="${m}">${monthNames[m]}</option>`;
      });
      monthSelect.value = data.months.includes(defaultMonth) ? defaultMonth : "";
    });
}

function updateAllCharts(year, month = "") {
  fetch(`/guests/ajax/chart-data/?year=${year}&month=${month}`)
    .then(res => res.json())
    .then(data => {
      // Guest Entry Trend
      new ApexCharts(document.querySelector("#chart-guest-entry"), {
        chart: { type: 'bar', height: 250 },
        series: [{ name: 'Guests', data: data.monthly.counts }],
        xaxis: { categories: data.monthly.labels }
      }).render();

      // Services Attended
      new ApexCharts(document.querySelector("#services-attended-chart"), {
        chart: { type: 'bar', height: 300 },
        series: [{ name: 'Services', data: data.services.counts }],
        xaxis: { categories: data.services.labels }
      }).render();

      // Mini Total Guest Trend
      new ApexCharts(document.querySelector("#chart-visitors"), {
        chart: { type: 'line', height: 80, sparkline: { enabled: true } },
        series: [{ name: 'Visitors', data: data.monthly.counts }],
        stroke: { width: 2, curve: 'smooth' },
        colors: ["#206bc4"]
      }).render();

      // Status Chart Center Count Update
      const totalStatus = data.status.counts.reduce((a, b) => a + b, 0);
      document.getElementById("statusChartCenterText").innerHTML = `Total<br>${totalStatus}`;

      // Guest Status Chart
      new Chart(document.getElementById("statusChart"), {
        type: 'doughnut',
        data: {
          labels: data.status.labels,
          datasets: [{
            label: 'Guest Status',
            data: data.status.counts,
            backgroundColor: ['#2fb344', '#f76707', '#d63939', '#4263eb']
          }]
        },
        options: {
          responsive: true,
          cutout: '65%',
          plugins: {
            legend: { display: true, position: 'bottom' },
            tooltip: { enabled: true }
          }
        }
      });

      // Channel Table
      const table = document.getElementById("channelProgressTableBody");
      table.innerHTML = "";
      data.channels.forEach(({ label, count, percent }) => {
        table.innerHTML += `
          <tr>
            <td>${label}</td>
            <td>${count}</td>
            <td class="w-50">
              <div class="progress progress-xs">
                <div class="progress-bar bg-primary" style="width: ${percent}%"></div>
              </div>
            </td>
          </tr>`;
      });
    });
}

document.addEventListener("DOMContentLoaded", () => {
  const yearSelect = document.getElementById("dashboardYearSelect") || document.getElementById("monthlyYearSelect");
  const monthSelect = document.getElementById("dashboardMonthSelect") || document.getElementById("monthlyMonthSelect");

  loadYearsAndCurrent(yearSelect.id, (year, currentMonth) => {
    loadMonths(monthSelect.id, year, currentMonth).then(() => {
      updateAllCharts(year, currentMonth);
    });
  });

  yearSelect.addEventListener("change", async () => {
    const year = yearSelect.value;
    await loadMonths(monthSelect.id, year);
    updateAllCharts(year, monthSelect.value);
  });

  monthSelect.addEventListener("change", () => {
    updateAllCharts(yearSelect.value, monthSelect.value);
  });
});
</script>

{% endblock %}
         
<!-- ApexCharts -->
<script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>



<header class="navbar navbar-expand-md d-print-none">
          <div class="container-xl">
            <!-- BEGIN NAVBAR TOGGLER -->
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-menu" aria-controls="navbar-menu" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <!-- END NAVBAR TOGGLER -->
            <!-- BEGIN NAVBAR LOGO -->
            <div class="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
              <a href="/" class="navbar-brand d-flex align-items-center">
                <img src="{% static 'images/church_logo.png' %}" alt="Logo" width="50" height="50" class="me-2">
                <span class="text-white fw-bold"></span>
              </a>
            </div>
            <!-- END NAVBAR LOGO -->

            <!-- Scrolling Banner -->
            <div class="header-banner bg-dark text-warning shadow-sm me-6">
              <div class="scrolling-text">
                <strong>WE EXIST TO RAISE FULLY DEVOTED FOLLOWERS OF CHRIST, TO BECOME SIGNIFICANT IN LIFE AND THE MARKETPLACE.</strong>
              </div>
            </div>


            <div class="navbar-nav flex-row order-md-last">
              <div class="nav-item d-none d-md-flex me-3">
                <div class="btn-list">
                  <a href="https://gatewaynation.org" class="btn btn-5" target="_blank" rel="noreferrer">
                    <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="currentColor"  class="icon icon-tabler icons-tabler-filled icon-tabler-pointer">
                      <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                      <path d="M3.039 4.277l3.904 13.563c.185 .837 .92 1.516 1.831 1.642l.17 .016a2.2 2.2 0 0 0 1.982 -1.006l.045 -.078l1.4 -2.072l4.05 4.05a2.067 2.067 0 0 0 2.924 0l1.047 -1.047c.388 -.388 .606 -.913 .606 -1.461l-.008 -.182a2.067 2.067 0 0 0 -.598 -1.28l-4.047 -4.048l2.103 -1.412c.726 -.385 1.18 -1.278 1.053 -2.189a2.2 2.2 0 0 0 -1.701 -1.845l-13.524 -3.89a1 1 0 0 0 -1.236 1.24z" />
                    </svg>
                    Gateway Nation
                  </a>
                </div>
              </div>
              <div class="d-none d-md-flex">
                <div class="nav-item">
                  <a href="?theme=dark" class="nav-link px-0 hide-theme-dark" data-bs-toggle="tooltip" data-bs-placement="bottom" aria-label="Enable dark mode" data-bs-original-title="Enable dark mode">
                    <!-- Download SVG icon from http://tabler.io/icons/icon/moon -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                      <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z"></path>
                    </svg>
                  </a>
                  <a href="?theme=light" class="nav-link px-0 hide-theme-light" data-bs-toggle="tooltip" data-bs-placement="bottom" aria-label="Enable light mode" data-bs-original-title="Enable light mode">
                    <!-- Download SVG icon from http://tabler.io/icons/icon/sun -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                      <path d="M12 12m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"></path>
                      <path d="M3 12h1m8 -9v1m8 8h1m-9 8v1m-6.4 -15.4l.7 .7m12.1 -.7l-.7 .7m0 11.4l.7 .7m-12.1 -.7l-.7 .7"></path>
                    </svg>
                  </a>
                </div>
                <div class="nav-item dropdown d-none d-md-flex me-3">
                  <a href="#" class="nav-link px-0" data-bs-toggle="dropdown" tabindex="-1" aria-label="Show app menu" data-bs-auto-close="outside" aria-expanded="false">
                    <!-- Download SVG icon from http://tabler.io/icons/icon/apps -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                      <path d="M4 4m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"></path>
                      <path d="M4 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"></path>
                      <path d="M14 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"></path>
                      <path d="M14 7l6 0"></path>
                      <path d="M17 4l0 6"></path>
                    </svg>
                  </a>
                  <div class="dropdown-menu dropdown-menu-arrow dropdown-menu-end dropdown-menu-card">
                    <div class="card">
                      <div class="card-header">
                        <div class="card-title">My Apps</div>
                        <div class="card-actions btn-actions">
                          <a href="#" class="btn-action">
                            <!-- Download SVG icon from http://tabler.io/icons/icon/settings -->
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                              <path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z"></path>
                              <path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"></path>
                            </svg>
                          </a>
                        </div>
                      </div>
                      <div class="card-body scroll-y p-2" style="max-height: 50vh">
                        <div class="row g-0">
                          <div class="col-4">
                            <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" id="Google-Drive--Streamline-Svg-Logos" height="24" width="24">
                              <desc>
                                Google Drive Streamline Icon: https://streamlinehq.com
                              </desc>
                              <path fill="#0066da" d="m2.02664 19.49685 1.036385 1.7901c0.215325 0.376875 0.524875 0.672975 0.8883 0.888325 1.040875 -1.321275 1.76545 -2.3352 2.173675 -3.041825 0.414275 -0.717075 0.9235 -1.838675 1.52765 -3.364825 -1.6281 -0.214275 -2.861875 -0.321425 -3.701325 -0.321425 -0.805575 0 -2.03935 0.10715 -3.701325 0.321425 0 0.41725 0.107675 0.834475 0.323025 1.21135l1.453615 2.516875Z" stroke-width="0.25"></path>
                              <path fill="#ea4335" d="M20.0487 22.175275c0.363425 -0.21535 0.672975 -0.51145 0.8883 -0.888325l0.430725 -0.74025 2.05925 -3.566725C23.642325 16.6031 23.75 16.185875 23.75 15.768625c-1.671575 -0.214275 -2.903125 -0.321425 -3.694575 -0.321425 -0.850575 0 -2.0821 0.10715 -3.694575 0.321425 0.597 1.5345 1.099475 2.656125 1.50745 3.364825 0.41155 0.714975 1.13835 1.728925 2.1804 3.041825Z" stroke-width="0.25"></path>
                              <path fill="#00832d" d="M12.00005 8.231375c1.20435 -1.45455 2.03435 -2.576175 2.489975 -3.364825 0.366875 -0.63505 0.77065 -1.648975 1.211325 -3.04181 -0.3634 -0.21535 -0.78065 -0.3230225 -1.211325 -0.3230225H9.51005c-0.4307 0 -0.847925 0.1211325 -1.21135 0.3230225 0.560525 1.597435 1.03615 2.73431 1.4269 3.410635 0.431775 0.747375 1.189925 1.74605 2.27445 2.996Z" stroke-width="0.25"></path>
                              <path fill="#2684fc" d="M16.347225 15.768625h-8.69475L3.951175 22.17525c0.3634 0.21535 0.78065 0.323025 1.21135 0.323025h13.674675c0.4307 0 0.84795 -0.121125 1.21135 -0.323025L16.347225 15.768625Z" stroke-width="0.25"></path>
                              <path fill="#00ac47" d="M12 8.2314 8.2987 1.824745c-0.3634 0.2153475 -0.673 0.5114425 -0.888325 0.88833L0.573025 14.557275C0.357675 14.93415 0.25 15.3514 0.25 15.768625h7.40265L12 8.2314Z" stroke-width="0.25"></path>
                              <path fill="#ffba00" d="M20.0083 8.635175 16.589625 2.713075c-0.215325 -0.3768875 -0.5249 -0.6729825 -0.888325 -0.88833L12 8.2314l4.34735 7.537225h7.3892c0 -0.417225 -0.107675 -0.834475 -0.323025 -1.21135L20.0083 8.635175Z" stroke-width="0.25"></path>
                            </svg>
                              <span class="h5">Google Drive</span>          
                            </a>
                          </div>
                          <div class="col-4">
                            <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" id="Google-Meet--Streamline-Svg-Logos" height="24" width="24">
                                <desc>
                                  Google Meet Streamline Icon: https://streamlinehq.com
                                </desc>
                                <path fill="#00832d" d="m13.544075 12 2.2909 2.61865 3.080875 1.9686 0.535875 -4.5707 -0.535875 -4.4676 -3.13985 1.729275L13.544075 12Z" stroke-width="0.25"></path>
                                <path fill="#0066da" d="M0.2501225 16.161825V20.05675c0 0.88935 0.7218175 1.61135 1.6113475 1.61135H5.756375l0.806525 -2.942825 -0.806525 -2.56345 -2.67215 -0.806525 -2.8341025 0.806525Z" stroke-width="0.25"></path>
                                <path fill="#e94235" d="M5.75625 2.3319025 0.25 7.838175l2.83425 0.80465 2.672 -0.80465 0.791875 -2.5285L5.75625 2.3319025Z" stroke-width="0.25"></path>
                                <path fill="#2684fc" d="M0.2501225 16.163625H5.756375V7.8381H0.2501225v8.325525Z" stroke-width="0.25"></path>
                                <path fill="#00ac47" d="m22.43315 4.6633 -3.517375 2.88575v9.038125l3.53205 2.896975c0.5287 0.414175 1.30215 0.03665 1.30215 -0.6354V5.28575c0 -0.67955 -0.79185 -1.0552 -1.316825 -0.62245Z" stroke-width="0.25"></path>
                                <path fill="#00ac47" d="M13.544 12v4.161825H5.756225v5.506275h11.548225c0.889525 0 1.61135 -0.722 1.61135 -1.61135V16.58725L13.544 12Z" stroke-width="0.25"></path>
                                <path fill="#ffba00" d="M17.30445 2.3319025H5.756225V7.838175H13.544V12l5.3718 -4.451075V3.94325c0 -0.889525 -0.721825 -1.6113475 -1.61135 -1.6113475Z" stroke-width="0.25"></path>
                              </svg>
                              <span class="h5">Google Meet</span>
                            </a>
                          </div>                        
                          <div class="col-4">
                            <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                              <style>
                                .whatsapp-icon {
                                  color: #25D366; /* Google Drive green or any hex color */
                                }
                              </style>
                              <svg class="whatsapp-icon" xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-brand-whatsapp">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 21l1.65 -3.8a9 9 0 1 1 3.4 2.9l-5.05 .9" />
                                <path d="M9 10a.5 .5 0 0 0 1 0v-1a.5 .5 0 0 0 -1 0v1a5 5 0 0 0 5 5h1a.5 .5 0 0 0 0 -1h-1a.5 .5 0 0 0 0 1" />
                              </svg>
                              <span class="h5">WhatsApp</span>
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="nav-item dropdown">
                <a href="#" class="nav-link d-flex lh-1 p-0 px-2" data-bs-toggle="dropdown" aria-label="Open user menu">
                  <span class="avatar avatar-sm" style="background-image: url('{{ user.profile.image.url }}')"> </span>
                  <div class="d-none d-xl-block ps-2">
                    <div>{{ user.get_full_name|default:user.username }}</div>
                    <div class="mt-1 small text-secondary">
                      {% if user.is_superuser %}
                        Superuser
                      {% elif user.groups.first %}
                        {{ user.groups.first.name }}
                      {% else %}
                        No Group
                      {% endif %}
                    </div>
                  </div>
                </a>
                <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
                  <!--
                  <a href="#" class="dropdown-item">Status</a>
                  <a href="./profile.html" class="dropdown-item">Profile</a>
                  <a href="#" class="dropdown-item">Feedback</a>
                  <div class="dropdown-divider"></div>
                  <a href="./settings.html" class="dropdown-item">Settings</a>
                  -->
                  <a href="{% url 'login' %}" class="dropdown-item bg-danger">Logout</a>
                </div>
              </div>
            </div>
          </div>
        </header>
        <header class="navbar-expand-md">
          <div class="collapse navbar-collapse" id="navbar-menu">
            <div class="navbar">
              <div class="container-xl">
                <div class="row flex-column flex-md-row flex-fill align-items-center">
                  <div class="col">
                    <!-- BEGIN NAVBAR MENU -->
                    <ul class="navbar-nav">
                      <li class="nav-item">
                        <a class="nav-link text-white me-2" href="./">
                          <span class="nav-link-icon d-md-none d-lg-inline-block"><!-- Download SVG icon from http://tabler.io/icons/icon/home -->
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                              <path d="M5 12l-2 0l9 -9l9 9l-2 0"></path>
                              <path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7"></path>
                              <path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6"></path></svg></span>
                          <span class="nav-link-title"> Dashboard </span>
                        </a>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link text-white" href="{% url 'guest_list' %}">
                          <span class="nav-link-icon d-md-none d-lg-inline-block"><!-- Download SVG icon from http://tabler.io/icons/icon/home -->
                            <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-users">
                              <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" /><path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /><path d="M21 21v-2a4 4 0 0 0 -3 -3.85" />
                            </svg>
                          </span>
                          <span class="nav-link-title"> Guests </span>
                        </a>
                    </ul>
                    <!-- END NAVBAR MENU -->
                  </div>
                  <div class="col col-md-auto">
                    <ul class="navbar-nav">
                      <li class="nav-item">
                        <div class="dropdown">
                          <button class="btn dropdown-toggle d-flex align-items-center" data-bs-toggle="dropdown">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-2">
                              <path d="M12 5l0 14"></path>
                              <path d="M5 12l14 0"></path>
                            </svg>
                            Records
                          </button>
                          <div class="dropdown-menu shadow-sm" style="min-width: 100px;">
                            <div class="col-auto flex-column d-flex gap-2">
                              <a href="{% url 'create_guest' %}" class="btn btn-success d-flex align-items-center">
                                <i class="bi bi-person-plus-fill me-1"></i> Add Guest
                              </a>
                              {% if is_admin_group or request.user.is_superuser %}
                              <a href="{% url 'create_user' %}" class="btn btn-secondary d-flex align-items-center">
                                <i class="bi bi-person-badge-fill me-1"></i> Add User
                              </a>
                              {% endif %}
                              <button class="btn bg-dark shadow-lg d-flex flex-wrap gap-2 align-items-center justify-content-end" data-chart="myChart">
                                <i class="ti ti-photo"></i> Export PNG
                              </button>
                            </div>
                          </div>
                        </div>
                      </li>
                      <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle me-2 bg-dark text-white shadow-lg" href="#navbar-base" data-bs-toggle="dropdown" data-bs-auto-close="outside" role="button" aria-expanded="false">
                          <span class="nav-link-icon d-md-none d-lg-inline-block"><!-- Download SVG icon from http://tabler.io/icons/icon/package -->
                            <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="currentColor"  class="icon icon-tabler icons-tabler-filled icon-tabler-filters">
                              <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M19.396 11.056a6 6 0 0 1 -5.647 10.506q .206 -.21 .396 -.44a8 8 0 0 0 1.789 -6.155a8.02 8.02 0 0 0 3.462 -3.911" />
                              <path d="M4.609 11.051a7.99 7.99 0 0 0 9.386 4.698a6 6 0 1 1 -9.534 -4.594z" /><path d="M12 2a6 6 0 1 1 -6 6l.004 -.225a6 6 0 0 1 5.996 -5.775" />
                            </svg>
                          </span>
                          <span class="nav-link-title"> Filters </span>
                        </a>
                        <style>
                          /* Enable hover to open dropdown */
                          .dropdown-menu .dropend:hover > .dropdown-menu {
                            display: block;
                            margin-left: 0.1rem;
                          }
                          .dropdown-menu .dropend > .dropdown-toggle::after {
                            margin-left: 0.5rem;
                          }
                          .dropdown-menu .dropend .dropdown-menu {
                            top: 0;
                            left: 100%;
                            margin-top: -0.5rem;
                          }
                        </style>
                        <div class="dropdown-menu">

                          <!-- Channel of Visit -->
                          <div class="dropend">
                            <a class="dropdown-item dropdown-toggle" href="#" role="button">Channel of Visit</a>
                            <div class="dropdown-menu">
                              {% for channel in channels %}
                                <a href="?channel={{ channel|urlencode }}" class="dropdown-item">{{ channel }}</a>
                              {% endfor %}
                            </div>
                          </div>

                          <!-- Guest Status -->
                          <div class="dropend">
                            <a class="dropdown-item dropdown-toggle" href="#" role="button">Guest Status</a>
                            <div class="dropdown-menu">
                              {% for status in statuses %}
                                <a href="?status={{ status|urlencode }}" class="dropdown-item">{{ status }}</a>
                              {% endfor %}
                            </div>
                          </div>

                          <!-- Purpose of Visit -->
                          <div class="dropend">
                            <a class="dropdown-item dropdown-toggle" href="#" role="button">Purpose of Visit</a>
                            <div class="dropdown-menu">
                              {% for purpose in purposes %}
                                <a href="?purpose={{ purpose|urlencode }}" class="dropdown-item">{{ purpose }}</a>
                              {% endfor %}
                            </div>
                          </div>

                          <!-- Service Attended -->
                          <div class="dropend">
                            <a class="dropdown-item dropdown-toggle" href="#" role="button">Service Attended</a>
                            <div class="dropdown-menu">
                              {% for service in services %}
                                <a href="?service={{ service|urlencode }}" class="dropdown-item">{{ service }}</a>
                              {% endfor %}
                            </div>
                          </div>

                        </div>

                      </li>
                      <li class="nav-item">
                        <!-- Search Form -->
                        <form method="get" class="d-flex" style="gap: 6px;">
                          <input type="hidden" name="user" value="{{ request.GET.user }}">
                          <input type="hidden" name="service" value="{{ request.GET.service }}">
                          <input type="search" name="q" class="form-control d-flex flex-wrap gap-2 align-items-center justify-content-end" style="width: 160px;" placeholder="Search guests..." value="{{ request.GET.q }}">
                          <button type="submit" class="btn btn-sm btn-outline d-flex flex-wrap gap-2 align-items-center justify-content-end"><i class="bi bi-search"></i></button>
                        </form>
                      </li>
                      <li class="nav-item ms-1">
                        <!-- Reset Button -->
                        <a href="{% url 'guest_list' %}" class="btn btn-sm btn-outline d-flex flex-wrap gap-2 align-items-center justify-content-end">
                          Reset
                        </a>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </header>
      </div>
      <div class="mobile-navbar">
        <header class="navbar navbar-expand-md navbar-dark bg-dark sticky-top">
          <div class="container-fluid d-flex align-items-center">

            <!-- Logo -->
            <a href="/" class="navbar-brand d-flex align-items-center">
              <img src="{% static 'images/church_logo.png' %}" alt="Logo" width="40" height="40" class="me-2">
              <span class="fw-bold text-white"></span>
            </a>

            <!-- Scrolling Banner -->
            <div class="flex-fill mx-2">
              <div class="header-banner bg-dark text-warning shadow-sm">
                <div class="scrolling-text">
                  <strong>
                    WE EXIST TO RAISE FULLY DEVOTED FOLLOWERS OF CHRIST, TO BECOME SIGNIFICANT IN LIFE AND THE MARKETPLACE.
                  </strong>
                </div>
              </div>
            </div>

            <!-- User avatar (right side) -->
            <a href="#" class="ms-auto me-2" data-bs-toggle="dropdown">
              <span class="avatar avatar-sm" style="background-image: url('{{ user.profile.image.url }}')"></span>
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><a class="dropdown-item" href="./">Dashboard</a></li>
              <li><a class="dropdown-item" href="{% url 'guest_list' %}">Guests</a></li>
              <li><a class="dropdown-item" href="https://gatewaynation.org" target="_blank">Gateway Nation</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item text-danger" href="{% url 'login' %}">Logout</a></li>
            </ul>

            <!-- Toggler -->
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mobileNavbarMenu">
              <span class="navbar-toggler-icon"></span>
            </button>

            <!-- Collapsible menu -->
            <div class="collapse navbar-collapse" id="mobileNavbarMenu">

              <!-- Links -->
              <ul class="navbar-nav mt-2">
                <li class="nav-item"><a class="nav-link" href="./">Dashboard</a></li>
                <li class="nav-item"><a class="nav-link" href="{% url 'guest_list' %}">Guests</a></li>

                <li class="nav-item">
                  <div class="dropdown">
                    <button class="btn dropdown-toggle d-flex align-items-center" data-bs-toggle="dropdown">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-2">
                        <path d="M12 5l0 14"></path>
                        <path d="M5 12l14 0"></path>
                      </svg>
                      Records
                    </button>
                    <div class="dropdown-menu shadow-sm" style="min-width: 60px;">
                      <div class="col-auto flex-column d-flex gap-2">
                        <a href="{% url 'create_guest' %}" class="btn btn-success d-flex align-items-center">
                          <i class="bi bi-person-plus-fill me-1"></i> Add Guest
                        </a>
                        {% if is_admin_group or request.user.is_superuser %}
                        <a href="{% url 'create_user' %}" class="btn btn-secondary d-flex align-items-center">
                          <i class="bi bi-person-badge-fill me-1"></i> Add User
                        </a>
                        {% endif %}
                        <button class="btn bg-dark shadow-lg d-flex flex-wrap gap-2 align-items-center justify-content-end" data-chart="myChart">
                          <i class="ti ti-photo"></i> Export PNG
                        </button>
                      </div>
                    </div>
                  </div>
                </li>



    <div class="desktop-navbar">
        <header class="navbar navbar-expand-md unified-header d-print-none">
          <div class="container-xl">
            <!-- BEGIN NAVBAR TOGGLER -->
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-menu" aria-controls="navbar-menu" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <!-- END NAVBAR TOGGLER -->
            <!-- BEGIN NAVBAR LOGO -->
            <div class="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
              <a href="/" class="navbar-brand d-flex align-items-center">
                <img src="{% static 'images/church_logo.png' %}" alt="Logo" width="60" height="60" class="me-2">
                <span class="text-white fw-bold"></span>
              </a>
            </div>
            <!-- END NAVBAR LOGO -->

            
            <div class="dropdown">
              <button class="btn d-flex align-items-center" data-bs-toggle="dropdown">
                <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-menu-4">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                  <path d="M7 6h10" /><path d="M4 12h16" /><path d="M7 12h13" /><path d="M7 18h10" />
                </svg>
                Menu
              </button>
              <div class="dropdown-menu shadow-sm" style="max-width: 100px;">
                <div class="col-auto flex-column d-flex">
                  <a href="./" class="dropdown-item d-flex align-items-center">
                    <span class="nav-link-icon d-md-none d-lg-inline-block"><!-- Download SVG icon from http://tabler.io/icons/icon/home -->
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                        <path d="M5 12l-2 0l9 -9l9 9l-2 0"></path>
                        <path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7"></path>
                        <path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6"></path></svg></span>
                    <span class="nav-link-title"> Dashboard </span>
                  </a>
                  <a href="{% url 'guest_list' %}" class="dropdown-item text-green d-flex align-items-center">
                    <span class="nav-link-icon d-md-none d-lg-inline-block"><!-- Download SVG icon from http://tabler.io/icons/icon/home -->
                      <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-users">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" /><path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /><path d="M21 21v-2a4 4 0 0 0 -3 -3.85" />
                      </svg>
                    </span>
                    <span class="nav-link-title"> Guests </span>
                  </a>
                </div>
              </div>
            </div>

            <!-- Scrolling Banner -->
            <div class="header-banner bg-dark text-warning shadow-sm ms-1 me-1">
              <div class="scrolling-text">
                <strong>WE EXIST TO RAISE FULLY DEVOTED FOLLOWERS OF CHRIST, TO BECOME SIGNIFICANT IN LIFE AND THE MARKETPLACE.</strong>
              </div>
            </div>


            <div class="navbar-nav flex-row order-md-last">
              <li class="nav-item">
                <div class="dropdown">
                  <button class="btn d-flex align-items-center" data-bs-toggle="dropdown">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-2">
                      <path d="M12 5l0 14"></path>
                      <path d="M5 12l14 0"></path>
                    </svg>
                    Records
                  </button>
                  <div class="dropdown-menu shadow-sm" style="min-width: 100px;">
                    <div class="col-auto flex-column d-flex">
                      <a href="{% url 'create_guest' %}" class="dropdown-item text-success d-flex align-items-center">
                        <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-users-plus">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M5 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" />
                          <path d="M3 21v-2a4 4 0 0 1 4 -4h4c.96 0 1.84 .338 2.53 .901" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /><path d="M16 19h6" /><path d="M19 16v6" />
                        </svg>
                        Add Guest
                      </a>
                      {% if is_admin_group or request.user.is_superuser %}
                      <a href="{% url 'create_user' %}" class="dropdown-item text-warning d-flex align-items-center">
                        <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-user-plus">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" /><path d="M16 19h6" /><path d="M19 16v6" />
                          <path d="M6 21v-2a4 4 0 0 1 4 -4h4" />
                        </svg>
                        Add User
                      </a>
                      {% endif %}
                      <a class="dropdown-item shadow-lg d-flex align-items-center" data-chart="myChart">
                        <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-file-export">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M14 3v4a1 1 0 0 0 1 1h4" />
                          <path d="M11.5 21h-4.5a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v5m-5 6h7m-3 -3l3 3l-3 3" />
                        </svg>
                        Export PNG
                      </a>
                    </div>
                  </div>
                </div>
              </li>
              <div class="d-none d-md-flex">
                <div class="nav-item ms-2 me-2">
                  <a href="?theme=dark" class="nav-link px-0 hide-theme-dark" data-bs-toggle="tooltip" data-bs-placement="bottom" aria-label="Enable dark mode" data-bs-original-title="Enable dark mode">
                    <!-- Download SVG icon from http://tabler.io/icons/icon/moon -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                      <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z"></path>
                    </svg>
                  </a>
                  <a href="?theme=light" class="nav-link px-0 hide-theme-light" data-bs-toggle="tooltip" data-bs-placement="bottom" aria-label="Enable light mode" data-bs-original-title="Enable light mode">
                    <!-- Download SVG icon from http://tabler.io/icons/icon/sun -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                      <path d="M12 12m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"></path>
                      <path d="M3 12h1m8 -9v1m8 8h1m-9 8v1m-6.4 -15.4l.7 .7m12.1 -.7l-.7 .7m0 11.4l.7 .7m-12.1 -.7l-.7 .7"></path>
                    </svg>
                  </a>
                </div>
                <div class="nav-item dropdown d-none d-md-flex me-1">
                  <a href="#" class="nav-link px-0" data-bs-toggle="dropdown" tabindex="-1" aria-label="Show app menu" data-bs-auto-close="outside" aria-expanded="false">
                    <!-- Download SVG icon from http://tabler.io/icons/icon/apps -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                      <path d="M4 4m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"></path>
                      <path d="M4 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"></path>
                      <path d="M14 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"></path>
                      <path d="M14 7l6 0"></path>
                      <path d="M17 4l0 6"></path>
                    </svg>
                  </a>
                  <div class="dropdown-menu dropdown-menu-arrow dropdown-menu-end dropdown-menu-card">
                    <div class="card">
                      <div class="card-header">
                        <div class="card-title">My Apps</div>
                        <div class="card-actions btn-actions">
                          <a href="#" class="btn-action">
                            <!-- Download SVG icon from http://tabler.io/icons/icon/settings -->
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-1">
                              <path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z"></path>
                              <path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"></path>
                            </svg>
                          </a>
                        </div>
                      </div>
                      <div class="card-body scroll-y p-2" style="max-height: 50vh">
                        <div class="row g-0">
                          <div class="col-4">
                            <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" id="Google-Drive--Streamline-Svg-Logos" height="24" width="24">
                              <desc>
                                Google Drive Streamline Icon: https://streamlinehq.com
                              </desc>
                              <path fill="#0066da" d="m2.02664 19.49685 1.036385 1.7901c0.215325 0.376875 0.524875 0.672975 0.8883 0.888325 1.040875 -1.321275 1.76545 -2.3352 2.173675 -3.041825 0.414275 -0.717075 0.9235 -1.838675 1.52765 -3.364825 -1.6281 -0.214275 -2.861875 -0.321425 -3.701325 -0.321425 -0.805575 0 -2.03935 0.10715 -3.701325 0.321425 0 0.41725 0.107675 0.834475 0.323025 1.21135l1.453615 2.516875Z" stroke-width="0.25"></path>
                              <path fill="#ea4335" d="M20.0487 22.175275c0.363425 -0.21535 0.672975 -0.51145 0.8883 -0.888325l0.430725 -0.74025 2.05925 -3.566725C23.642325 16.6031 23.75 16.185875 23.75 15.768625c-1.671575 -0.214275 -2.903125 -0.321425 -3.694575 -0.321425 -0.850575 0 -2.0821 0.10715 -3.694575 0.321425 0.597 1.5345 1.099475 2.656125 1.50745 3.364825 0.41155 0.714975 1.13835 1.728925 2.1804 3.041825Z" stroke-width="0.25"></path>
                              <path fill="#00832d" d="M12.00005 8.231375c1.20435 -1.45455 2.03435 -2.576175 2.489975 -3.364825 0.366875 -0.63505 0.77065 -1.648975 1.211325 -3.04181 -0.3634 -0.21535 -0.78065 -0.3230225 -1.211325 -0.3230225H9.51005c-0.4307 0 -0.847925 0.1211325 -1.21135 0.3230225 0.560525 1.597435 1.03615 2.73431 1.4269 3.410635 0.431775 0.747375 1.189925 1.74605 2.27445 2.996Z" stroke-width="0.25"></path>
                              <path fill="#2684fc" d="M16.347225 15.768625h-8.69475L3.951175 22.17525c0.3634 0.21535 0.78065 0.323025 1.21135 0.323025h13.674675c0.4307 0 0.84795 -0.121125 1.21135 -0.323025L16.347225 15.768625Z" stroke-width="0.25"></path>
                              <path fill="#00ac47" d="M12 8.2314 8.2987 1.824745c-0.3634 0.2153475 -0.673 0.5114425 -0.888325 0.88833L0.573025 14.557275C0.357675 14.93415 0.25 15.3514 0.25 15.768625h7.40265L12 8.2314Z" stroke-width="0.25"></path>
                              <path fill="#ffba00" d="M20.0083 8.635175 16.589625 2.713075c-0.215325 -0.3768875 -0.5249 -0.6729825 -0.888325 -0.88833L12 8.2314l4.34735 7.537225h7.3892c0 -0.417225 -0.107675 -0.834475 -0.323025 -1.21135L20.0083 8.635175Z" stroke-width="0.25"></path>
                            </svg>
                              <span class="h5"></span>          
                            </a>
                          </div>
                          <div class="col-4">
                            <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" id="Google-Meet--Streamline-Svg-Logos" height="24" width="24">
                                <desc>
                                  Google Meet Streamline Icon: https://streamlinehq.com
                                </desc>
                                <path fill="#00832d" d="m13.544075 12 2.2909 2.61865 3.080875 1.9686 0.535875 -4.5707 -0.535875 -4.4676 -3.13985 1.729275L13.544075 12Z" stroke-width="0.25"></path>
                                <path fill="#0066da" d="M0.2501225 16.161825V20.05675c0 0.88935 0.7218175 1.61135 1.6113475 1.61135H5.756375l0.806525 -2.942825 -0.806525 -2.56345 -2.67215 -0.806525 -2.8341025 0.806525Z" stroke-width="0.25"></path>
                                <path fill="#e94235" d="M5.75625 2.3319025 0.25 7.838175l2.83425 0.80465 2.672 -0.80465 0.791875 -2.5285L5.75625 2.3319025Z" stroke-width="0.25"></path>
                                <path fill="#2684fc" d="M0.2501225 16.163625H5.756375V7.8381H0.2501225v8.325525Z" stroke-width="0.25"></path>
                                <path fill="#00ac47" d="m22.43315 4.6633 -3.517375 2.88575v9.038125l3.53205 2.896975c0.5287 0.414175 1.30215 0.03665 1.30215 -0.6354V5.28575c0 -0.67955 -0.79185 -1.0552 -1.316825 -0.62245Z" stroke-width="0.25"></path>
                                <path fill="#00ac47" d="M13.544 12v4.161825H5.756225v5.506275h11.548225c0.889525 0 1.61135 -0.722 1.61135 -1.61135V16.58725L13.544 12Z" stroke-width="0.25"></path>
                                <path fill="#ffba00" d="M17.30445 2.3319025H5.756225V7.838175H13.544V12l5.3718 -4.451075V3.94325c0 -0.889525 -0.721825 -1.6113475 -1.61135 -1.6113475Z" stroke-width="0.25"></path>
                              </svg>
                              <span class="h5"></span>
                            </a>
                          </div>                        
                          <div class="col-4">
                            <a href="#" class="d-flex flex-column flex-center text-center text-secondary py-2 px-2 link-hoverable">
                              <style>
                                .whatsapp-icon {
                                  color: #25D366; /* Google Drive green or any hex color */
                                }
                              </style>
                              <svg class="whatsapp-icon" xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-brand-whatsapp">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M3 21l1.65 -3.8a9 9 0 1 1 3.4 2.9l-5.05 .9" />
                                <path d="M9 10a.5 .5 0 0 0 1 0v-1a.5 .5 0 0 0 -1 0v1a5 5 0 0 0 5 5h1a.5 .5 0 0 0 0 -1h-1a.5 .5 0 0 0 0 1" />
                              </svg>
                              <span class="h5"></span>
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="nav-item dropdown">
                <a href="#" class="nav-link d-flex lh-1 p-0 px-2 align-items-center" data-bs-toggle="dropdown" aria-label="Open user menu">
                  <span class="avatar avatar-sm" style="background-image: url('{{ user.profile.image.url }}')"> </span>
                  <div class="d-none d-xl-block ps-2">
                    <div>{{ user.get_full_name|default:user.username }}</div>
                    <div class="mt-1 small text-secondary">
                      {% if user.is_superuser %}
                        Superuser
                      {% elif user.groups.first %}
                        {{ user.groups.first.name }}
                      {% else %}
                        No Group
                      {% endif %}
                    </div>
                  </div>
                </a>
                <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow shadow-sm" style="min-width: 100px;">
                  <!--
                  <a href="#" class="dropdown-item">Status</a>
                  <a href="./profile.html" class="dropdown-item">Profile</a>
                  <a href="#" class="dropdown-item">Feedback</a>
                  <div class="dropdown-divider"></div>
                  <a href="./settings.html" class="dropdown-item">Settings</a>
                  -->
                  
                  <a href="https://gatewaynation.org" class="dropdown-item" target="_blank" rel="noreferrer">
                    <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-pointer">
                      <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                      <path d="M7.904 17.563a1.2 1.2 0 0 0 2.228 .308l2.09 -3.093l4.907 4.907a1.067 1.067 0 0 0 1.509 0l1.047 -1.047a1.067 1.067 0 0 0 0 -1.509l-4.907 -4.907l3.113 -2.09a1.2 1.2 0 0 0 -.309 -2.228l-13.582 -3.904l3.904 13.563z" />
                    </svg>
                    Gateway Nation
                  </a>
                  <a href="{% url 'login' %}" class="dropdown-item text-danger">
                    <svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-logout">
                      <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2" />
                      <path d="M9 12h12l-3 -3" /><path d="M18 15l3 -3" />
                    </svg>
                    Logout
                  </a>
                </div>
                
               
                
              </div>
            </div>
            
          </div>
        </header>
        
      </div>



{% endblock %}
